"""Command handlers. Each receives a list of string arguments."""

from exceptions import ExpenseError


def cmd_help(args: list[str]) -> None:
    print("Available commands:")
    print("  add <amount> <category>   Add a new expense")
    print("  list                      Show all expenses")
    print("  summary                   Show totals")
    print("  delete <id>               Remove an expense by ID")
    print("  help                      Show this help")
    print("  quit                      Exit the app")


def cmd_add(args: list[str]) -> None:
    print("[TODO] add — not implemented yet")


def cmd_list(args: list[str]) -> None:
    print("[TODO] list — not implemented yet")


def cmd_summary(args: list[str]) -> None:
    print("[TODO] summary — not implemented yet")


def cmd_delete(args: list[str]) -> None:
    print("[TODO] delete — not implemented yet")