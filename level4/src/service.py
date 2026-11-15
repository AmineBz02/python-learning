

from models import Library

def _prompt_int(msg: str) -> int:
    raw = input(msg).strip()
    try:
        return int(raw)
    except ValueError:
        raise ValueError(f"'{raw}' is not a valid number")


def _prompt_copies(msg: str) -> int:
    raw = input(msg).strip()
    if raw == "":
        return 1
    try:
        n = int(raw)
    except ValueError:
        raise ValueError(f"'{raw}' is not a valid number")
    if n < 0:
        raise ValueError("copies cannot be negative")
    return n



def handle_add_book(lib: Library) -> None:
    title = input("Title : ").strip()
    author = input("Author: ").strip()
    isbn = input("ISBN  : ").strip()
    copies = _prompt_copies("Copies [1]: ")
    if not title or not author or not isbn:
        raise ValueError("title, author and ISBN are required")
    lib.add_book(title, author, isbn, copies)
    print(f"✅ Added '{title}' (ISBN {isbn}) — {copies} copies")


def handle_register_member(lib: Library) -> None:
    name = input("Name: ").strip()
    if not name:
        raise ValueError("name is required")
    limit_raw = input("Borrow limit [3]: ").strip()
    limit = 3 if limit_raw == "" else _prompt_int("") or 3
    if limit <= 0:
        raise ValueError("limit must be positive")
    member = lib.register_member(name, limit)
    print(f"✅ Registered {member}")


def handle_borrow(lib: Library) -> None:
    isbn = input("ISBN      : ").strip()
    member_id = _prompt_int("Member id : ")
    lib.borrow(isbn, member_id)
    print(f"✅ Member #{member_id} borrowed '{isbn}'")


def handle_return(lib: Library) -> None:
    isbn = input("ISBN      : ").strip()
    member_id = _prompt_int("Member id : ")
    lib.return_book(isbn, member_id)
    print(f"✅ Member #{member_id} returned '{isbn}'")

