"""Plain data + the rules that belong to a single object."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal

LOAN_DAYS = 21
FINE_PER_DAY = Decimal("0.25")
MAX_FINE = Decimal("10.00")


class LendingError(Exception):
    """Business-rule violation (shown to the librarian)."""


@dataclass
class Book:
    isbn: str
    title: str
    copies: int = 1

    def __post_init__(self) -> None:
        digits = self.isbn.replace("-", "")
        if len(digits) != 13 or not digits.isdigit():
            raise LendingError(f"invalid ISBN-13 {self.isbn!r}")
        total = sum(int(d) * (3 if i % 2 else 1) for i, d in enumerate(digits))
        if total % 10:
            raise LendingError(f"ISBN checksum failed for {self.isbn!r}")
        self.isbn = digits


@dataclass
class Member:
    member_id: str
    name: str
    email: str
    max_loans: int = 3


@dataclass
class Loan:
    isbn: str
    member_id: str
    borrowed: date
    returned: date | None = None
    renewals: int = 0
    due: date = field(init=False)

    def __post_init__(self) -> None:
        self.due = self.borrowed + timedelta(days=LOAN_DAYS * (self.renewals + 1))

    def renew(self) -> None:
        if self.renewals >= 2:
            raise LendingError("a loan can be renewed at most twice")
        self.renewals += 1
        self.due += timedelta(days=LOAN_DAYS)

    def fine(self, on: date) -> Decimal:
        end = self.returned or on
        late = max(0, (end - self.due).days)
        return min(MAX_FINE, FINE_PER_DAY * late)
