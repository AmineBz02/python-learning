import sys
from commands import (
    cmd_add,
    cmd_delete,
    cmd_help,
    cmd_list,
    cmd_summary,
)
from exceptions import ExpenseError

# Map command name → handler
COMMANDS = {
    "add": cmd_add,
    "list": cmd_list,
    "summary": cmd_summary,
    "delete": cmd_delete,
    "help": cmd_help,
}


def main() -> None:
    print("Expense Tracker — type 'help' for commands")
    while True:
        try:
            raw = input("> ").strip()
            if not raw:
                continue

            parts = raw.split(maxsplit=1)
            print(f"DEBUG > parts :{parts}")
            cmd = parts[0].lower()
            args = parts[1].split() if len(parts) > 1 else []

            # Built-in quit
            if cmd in ("quit", "exit"):
                print("Bye!")
                break

            handler = COMMANDS.get(cmd)
            if handler is None:
                print(f"Unknown command: '{cmd}'. Type 'help' for a list.")
                continue

            handler(args)

        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break
        except ExpenseError as e:
            print(f"Error: {e}")
        except Exception as e:  # last-resort guard
            print(f"Unexpected error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()