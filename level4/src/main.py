"""
Library Management System — Level 4 OOP MVP
Run: python main.py

OOP concepts demonstrated:
  - Classes + __init__
  - Methods + self
  - Encapsulation (private attrs)
  - @property
  - Inheritance (custom exception hierarchy)
  - __str__ / __len__ dunder methods
"""

from __future__ import annotations

from service import handle_add_book, handle_borrow, handle_register_member, handle_return 
from models import Library
from exceptions import LibraryError

# ─────────────────────────────────────────────────────────────
# 5. CLI LAYER
# ─────────────────────────────────────────────────────────────
MENU = """
╔══════════════════════════════════╗
║     📚  LIBRARY MANAGEMENT       ║
╠══════════════════════════════════╣
║  1) Add book                     ║
║  2) Register member              ║
║  3) Borrow book                  ║
║  4) Return book                  ║
║  5) List books                   ║
║  6) List members                 ║
║  0) Exit                         ║
╚══════════════════════════════════╝"""




def main() -> None:
    lib = Library()
    actions = {
        "1": handle_add_book,
        "2": handle_register_member,
        "3": handle_borrow,
        "4": handle_return,
    }

    print("Welcome to the Library Management System!")
    while True:
        print(MENU)
        choice = input("> ").strip()

        try:
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "5":
                print(f"\n📚 Books ({len(lib)} total):")
                print(lib.list_books())
            elif choice == "6":
                print("\n👥 Members:")
                print(lib.list_members())
            elif choice in actions:
                actions[choice](lib)
            else:
                print("❌ Unknown option, try again.")
        except LibraryError as e:
            print(f"❌ {e}")
        except ValueError as e:
            print(f"❌ Invalid input: {e}")
        except KeyboardInterrupt:
            print("\n👋 Interrupted. Goodbye!")
            break


if __name__ == "__main__":
    main()