"""Custom exceptions for the Expense Tracker."""


class ExpenseError(Exception):
    """Base class for all expense-tracker errors."""


class ExpenseNotFound(ExpenseError):
    """Raised when an expense ID does not exist."""


class InvalidAmount(ExpenseError):
    """Raised when an amount is not a valid positive number."""