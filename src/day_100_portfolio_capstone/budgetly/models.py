"""Domain objects with validation at the boundary (exact money with Decimal)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation

CATEGORIES = ("food", "rent", "transport", "fun", "health", "other")


class BudgetError(Exception):
    """A user-facing error; the CLI turns it into a message and exit code 1."""


def parse_amount(text: str) -> Decimal:
    try:
        value = Decimal(text.replace(",", ".")).quantize(Decimal("0.01"))
    except InvalidOperation:
        raise BudgetError(f"not an amount: {text!r}") from None
    if value <= 0 or value > Decimal("1000000"):
        raise BudgetError("amount must be between 0.01 and 1,000,000")
    return value


@dataclass(frozen=True, slots=True)
class Expense:
    spent_on: date
    amount: Decimal
    category: str
    note: str = ""
    id: int | None = None

    def __post_init__(self) -> None:
        if self.category not in CATEGORIES:
            raise BudgetError(f"unknown category {self.category!r} (choose: {', '.join(CATEGORIES)})")
        if len(self.note) > 120:
            raise BudgetError("note is longer than 120 characters")
