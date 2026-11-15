"""Command handlers. Each receives a list of string arguments."""

from exceptions import ExpenseError
import service


def cmd_help(args: list[str]) -> None:
    print("Available commands:")
    print("  add <amount> <category>   Add a new expense")
    print("  list                      Show all expenses")
    print("  summary                   Show totals")
    print("  delete <id>               Remove an expense by ID")
    print("  help                      Show this help")
    print("  quit                      Exit the app")


def cmd_add(args: list[str]) -> None:
    if len(args) < 2:
        print("Usage: add <amount> <category>")
        return

    amount_str = args[0]
    category = " ".join(args[1:])   # support multi-word categories

    try:
        expense = service.add_expense(amount_str, category)
    except ExpenseError as e:
        print(f"Error: {e}")
        return

    print(f"Added expense #{expense.id}: {expense.amount:.2f} "
          f"[{expense.category}] on {expense.date}")

def cmd_list(args: list[str]) -> None:
    expenses = service.list_expenses()
    if not expenses:
        print("No expenses yet")
        return

    header = f"{'ID':>4}  {'DATE':<10}  {'AMOUNT':>10}  CATEGORY"
    print(header)
    print("-" * len(header))
    for e in expenses:
        print(f"{e.id:>4}  {e.date:<10}  {e.amount:>10.2f}  {e.category}")


def cmd_delete(args: list[str]) -> None:
    if len(args) != 1:
        print("Usage: delete <id>")
        return

    try:
        exp_id = int(args[0])
    except ValueError:
        print(f"Error: '{args[0]}' is not a valid ID (must be an integer)")
        return

    try:
        removed = service.delete_expense(exp_id)
    except ExpenseError as e:
        print(f"Error: {e}")
        return

    print(f"Deleted expense #{removed.id}: {removed.amount:.2f} "
          f"[{removed.category}] on {removed.date}")


def cmd_summary(args: list[str]) -> None:
    result = service.summary()

    print(f"Total: {result['total']:.2f}  ({result['count']} expenses)")

    if not result["by_category"]:
        return  # empty store — total of 0.00 already printed

    print("By category:")
    for cat, total in result["by_category"].items():
        print(f"  {cat:<16} {total:>10.2f}")