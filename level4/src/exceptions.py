# 1. EXCEPTION LAYER
# ─────────────────────────────────────────────────────────────
class LibraryError(Exception):
    """Base class for all library domain errors."""


class BookNotFound(LibraryError):
    """Raised when a book or member lookup fails."""


class BookUnavailable(LibraryError):
    """Raised when a book has no copies left."""


class MemberLimitReached(LibraryError):
    """Raised when a member has hit their borrow limit."""
