"""Business logic — to be implemented in EXP-4+."""
from datetime import date
from typing import Any

import storage
from exceptions import ExpenseNotFound, InvalidAmount, StorageError
from models import Expense

# Loaded once at import. Storage errors on startup are surfaced to main.py.
_state: dict[str, Any] = storage.load()


def _persist(new_state: dict[str, Any]) -> None:
    """Save first; only commit in-memory state if the write succeeded."""
    global _state
    storage.save(new_state)
    _state = new_state


def add_expense(amount_str: str, category: str) -> Expense:
    """Validate, build, persist a new Expense. Returns the created record.

    Raises:
        InvalidAmount: bad amount or empty category.
        StorageError: persistence failed; in-memory state is unchanged.
    """
    # --- Validate amount ---
    try:
        amount = float(amount_str)
    except (TypeError, ValueError):
        raise InvalidAmount(f"'{amount_str}' is not a number")

    if amount <= 0:
        raise InvalidAmount("Amount must be greater than zero")

    if amount != amount or amount == float("inf"):
        raise InvalidAmount("Amount must be a finite number")

    # --- Validate category ---
    category_clean = category.strip().lower()
    if not category_clean:
        raise InvalidAmount("Category cannot be empty")

    # --- Build record ---
    expense = Expense(
        id=_state["next_id"],
        amount=amount,          # rounded in __post_init__
        category=category_clean,
        date=date.today().isoformat(),
    )

    # --- Persist (save first, then commit) ---
    new_state = {
        "next_id": _state["next_id"] + 1,
        "expenses": _state["expenses"] + [expense.to_dict()],
    }
    _persist(new_state)

    return expense

def list_expenses() -> list[Expense]:
    """Return all expenses as Expense objects, in insertion order."""
    return [Expense.from_dict(d) for d in _state["expenses"]]


def delete_expense(exp_id: int) -> Expense:
    """Remove an expense by ID. Returns the deleted Expense.

    Raises:
        ExpenseNotFound: ID not present.
        StorageError: save failed; in-memory state is unchanged.
    """
    for i, d in enumerate(_state["expenses"]):
        if d["id"] == exp_id:
            removed = Expense.from_dict(d)
            new_state = {
                "next_id": _state["next_id"],
                "expenses": _state["expenses"].pop(i),
            }
            _persist(new_state)
            return removed
    raise ExpenseNotFound(f"No expense with id {exp_id}")


def summary() -> dict[str, object]:
    """Return {'total': float, 'by_category': {cat: total}, 'count': int}.

    by_category is sorted descending by total.
    """
    expenses = _state["expenses"]
    total = 0.0
    by_cat: dict[str, float] = {}

    for d in expenses:
        amt = float(d["amount"])
        total += amt
        cat = d["category"]
        by_cat[cat] = by_cat.get(cat, 0.0) + amt

    sorted_cats = dict(
        sorted(by_cat.items(), key=lambda kv: kv[1], reverse=True)
    )
    return {
        "total": round(total, 2),
        "count": len(expenses),
        "by_category": {k: round(v, 2) for k, v in sorted_cats.items()},
    }