"""Storage layer — to be implemented in EXP-3."""

import json
import os
import sys
from typing import Any

from exceptions import StorageError  # make sure this exists in exceptions.py

DATA_FILE = "expenses.json"


def _empty_state() -> dict[str, Any]:
    return {"next_id": 1, "expenses": []}


def _validate(data: Any) -> dict[str, Any]:
    """Reject any structure that doesn't match the expected schema."""
    if not isinstance(data, dict):
        raise ValueError("root is not an object")
    if not isinstance(data.get("expenses"), list):
        raise ValueError("'expenses' is not a list")
    if not isinstance(data.get("next_id"), int):
        raise ValueError("'next_id' is not an int")
    return data


def _backup_corrupt(path: str) -> None:
    """Preserve the corrupt file so the user can inspect it."""
    backup = path + ".corrupt"
    try:
        os.replace(path, backup)
        print(f"[storage] corrupt file backed up to {backup}", file=sys.stderr)
    except OSError as e:
        print(f"[storage] could not back up corrupt file: {e}", file=sys.stderr)


def load(path: str = DATA_FILE) -> dict[str, Any]:
    """Load state. Missing → empty. Corrupt → backed up + empty. Unreadable → StorageError."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return _validate(data)
    except FileNotFoundError:
        return _empty_state()
    except (json.JSONDecodeError, ValueError) as e:
        print(f"[storage] invalid data ({e})", file=sys.stderr)
        _backup_corrupt(path)
        return _empty_state()
    except OSError as e:
        raise StorageError(f"cannot read {path}: {e}") from e


def save(state: dict[str, Any], path: str = DATA_FILE) -> None:
    """Atomic write via temp file + os.replace. Raises StorageError on failure."""
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
            f.flush()
            os.fsync(f.fileno())   # durability before rename
        os.replace(tmp, path)
    except OSError as e:
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except OSError:
            pass
        raise StorageError(f"cannot write {path}: {e}") from e