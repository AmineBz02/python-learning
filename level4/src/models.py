from exceptions import BookNotFound, BookUnavailable, LibraryError, MemberLimitReached
# ─────────────────────────────────────────────────────────────
# 2. DOMAIN LAYER — Book
# ─────────────────────────────────────────────────────────────
class Book:
    def __init__(self, title: str, author: str, isbn: str, copies: int = 1) -> None:
        if copies < 0:
            raise ValueError("copies cannot be negative")
        self.title = title
        self.author = author
        self.isbn = isbn
        self.copies = copies

    @property
    def is_available(self) -> bool:
        return self.copies > 0

    def __str__(self) -> str:
        status = "available" if self.is_available else "unavailable"
        return f"'{self.title}' by {self.author} (ISBN {self.isbn}) — {self.copies} copies [{status}]"


# ─────────────────────────────────────────────────────────────
# 3. DOMAIN LAYER — Member
# ─────────────────────────────────────────────────────────────
class Member:
    def __init__(self, member_id: int, name: str, limit: int = 3) -> None:
        self.member_id = member_id
        self.name = name
        self.limit = limit
        self._borrowed: list[str] = []  # encapsulated

    @property
    def borrowed_count(self) -> int:
        return len(self._borrowed)

    @property
    def can_borrow(self) -> bool:
        return self.borrowed_count < self.limit

    def add_borrowed(self, isbn: str) -> None:
        self._borrowed.append(isbn)

    def remove_borrowed(self, isbn: str) -> None:
        if isbn not in self._borrowed:
            raise ValueError(f"'{isbn}' is not borrowed by {self.name}")
        self._borrowed.remove(isbn)

    def __str__(self) -> str:
        books = ", ".join(self._borrowed) if self._borrowed else "none"
        return f"#{self.member_id} {self.name} — {self.borrowed_count}/{self.limit} books [{books}]"


# ─────────────────────────────────────────────────────────────
# 4. DOMAIN LAYER — Library
# ─────────────────────────────────────────────────────────────
class Library:
    def __init__(self) -> None:
        self._books: dict[str, Book] = {}
        self._members: dict[int, Member] = {}
        self._next_id: int = 1

    # -- books --
    def add_book(self, title: str, author: str, isbn: str, copies: int = 1) -> Book:
        if isbn in self._books:
            # merge copies if same ISBN added again
            self._books[isbn].copies += copies
            return self._books[isbn]
        book = Book(title, author, isbn, copies)
        self._books[isbn] = book
        return book

    # -- members --
    def register_member(self, name: str, limit: int = 3) -> Member:
        member = Member(self._next_id, name, limit)
        self._members[self._next_id] = member
        self._next_id += 1
        return member

    # -- borrow / return --
    def borrow(self, isbn: str, member_id: int) -> None:
        book = self._books.get(isbn)
        if book is None:
            raise BookNotFound(f"No book with ISBN {isbn}")
        member = self._members.get(member_id)
        if member is None:
            raise BookNotFound(f"No member with id {member_id}")
        if not book.is_available:
            raise BookUnavailable(f"'{book.title}' has no copies left")
        if not member.can_borrow:
            raise MemberLimitReached(f"{member.name} reached limit {member.limit}")
        book.copies -= 1
        member.add_borrowed(isbn)

    def return_book(self, isbn: str, member_id: int) -> None:
        book = self._books.get(isbn)
        if book is None:
            raise BookNotFound(f"No book with ISBN {isbn}")
        member = self._members.get(member_id)
        if member is None:
            raise BookNotFound(f"No member with id {member_id}")
        member.remove_borrowed(isbn)  # raises ValueError if not borrowed
        book.copies += 1

    # -- listings --
    def list_books(self) -> str:
        if not self._books:
            return "  (no books yet)"
        return "\n".join(f"  {b}" for b in self._books.values())

    def list_members(self) -> str:
        if not self._members:
            return "  (no members yet)"
        return "\n".join(f"  {m}" for m in self._members.values())

    # -- dunder --
    def __len__(self) -> int:
        return len(self._books)

