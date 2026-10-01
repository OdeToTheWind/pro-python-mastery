"""Day 28 – Creating Classes in Python.

Scenario: a *community library catalogue* – a ``Book`` class with an
initialiser, instance attributes, behaviour methods and friendly dunders.

Deliverables (syllabus):
* Defining classes
* ``__init__``
* Instance attributes (vs class attributes)
* Methods (incl. ``__repr__``, ``__str__``, ``__eq__``)
"""

from __future__ import annotations

from datetime import date, timedelta

DELIVERABLES: dict[str, str] = {
    "defining a class": "Book",
    "__init__": "Book.__init__",
    "instance attributes": "Book.__init__",
    "class attributes": "Book.LOAN_DAYS",
    "methods": "Book.check_out",
    "dunder methods": "Book.__repr__",
}


class Book:
    """A single physical copy in the catalogue."""

    LOAN_DAYS = 14  # class attribute: shared by every Book
    copies_created = 0  # class attribute updated through the class, not self

    def __init__(self, title: str, author: str, isbn: str) -> None:
        if not title.strip() or not author.strip():
            raise ValueError("title and author are required")
        clean_isbn = isbn.replace("-", "")
        if not (clean_isbn.isdigit() and len(clean_isbn) == 13):
            raise ValueError("ISBN must have 13 digits")
        # instance attributes: different for every object
        self.title = title.strip()
        self.author = author.strip()
        self.isbn = clean_isbn
        self.borrower: str | None = None
        self.due: date | None = None
        Book.copies_created += 1

    @property
    def available(self) -> bool:
        return self.borrower is None

    def check_out(self, member: str, today: date) -> date:
        if not self.available:
            raise RuntimeError(f"{self.title!r} is already on loan to {self.borrower}")
        self.borrower = member
        self.due = today + timedelta(days=self.LOAN_DAYS)
        return self.due

    def return_book(self) -> None:
        if self.available:
            raise RuntimeError(f"{self.title!r} is not on loan")
        self.borrower = None
        self.due = None

    def days_overdue(self, today: date) -> int:
        if self.due is None:
            return 0
        return max(0, (today - self.due).days)

    def __repr__(self) -> str:
        return f"Book(title={self.title!r}, author={self.author!r}, isbn={self.isbn!r})"

    def __str__(self) -> str:
        state = "available" if self.available else f"due {self.due:%d %b}"
        return f"{self.title} by {self.author} – {state}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return self.isbn == other.isbn

    def __hash__(self) -> int:
        return hash(self.isbn)


def main() -> None:
    today = date(2026, 4, 9)
    print("Day 28 – Library catalogue\n")
    dune = Book("Dune", "Frank Herbert", "978-0-441-17271-9")
    emma = Book("Emma", "Jane Austen", "9780141439587")
    dune.check_out("Ravi", today)
    for book in (dune, emma):
        print(book)
    print(repr(emma))
    print("Overdue days on 1 May:", dune.days_overdue(date(2026, 5, 1)))
    print("Copies created so far:", Book.copies_created)


if __name__ == "__main__":
    main()
