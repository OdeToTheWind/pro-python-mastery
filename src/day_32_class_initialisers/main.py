"""Day 32 – Class Initialisers.

Scenario: *opening bank accounts* – the constructor is the gatekeeper that
guarantees every account object is valid from the first moment it exists.

Deliverables (syllabus):
* ``__init__`` constructors
* Defaults (incl. the mutable-default trap and ``default_factory``)
* Validation (reject, don't silently "fix")
* Object setup (derived attributes, unique IDs, ``__post_init__``)
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from decimal import Decimal

DELIVERABLES: dict[str, str] = {
    "__init__ constructor": "BankAccount.__init__",
    "defaults": "BankAccount.__init__",
    "validation in the constructor": "BankAccount.__init__",
    "object setup (ids, derived state)": "BankAccount.__init__",
    "mutable default trap": "BadAccount",
    "dataclass __post_init__": "SavingsGoal",
}

ACCOUNT_TYPES = ("savings", "current")
_account_numbers = itertools.count(1001)


class BankAccount:
    def __init__(
        self,
        owner: str,
        opening_balance: Decimal = Decimal("0"),
        account_type: str = "savings",
        transactions: list[Decimal] | None = None,
    ) -> None:
        owner = " ".join(owner.split())
        if not owner:
            raise ValueError("owner name is required")
        if opening_balance < 0:
            raise ValueError("opening balance cannot be negative")  # reject, don't clamp
        if account_type not in ACCOUNT_TYPES:
            raise ValueError(f"account_type must be one of {ACCOUNT_TYPES}")
        self.owner = owner
        self.account_type = account_type
        self.number = next(_account_numbers)  # unique ID assigned during setup
        # None-sentinel: every account gets its *own* new list
        self.transactions: list[Decimal] = list(transactions) if transactions else []
        if opening_balance:
            self.transactions.append(opening_balance)

    @property
    def balance(self) -> Decimal:
        return sum(self.transactions, Decimal("0"))

    def deposit(self, amount: Decimal) -> Decimal:
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.transactions.append(amount)
        return self.balance

    def withdraw(self, amount: Decimal) -> Decimal:
        if amount <= 0:
            raise ValueError("withdrawal must be positive")
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.transactions.append(-amount)
        return self.balance

    def __repr__(self) -> str:
        return f"BankAccount(#{self.number}, {self.owner!r}, {self.account_type}, balance={self.balance})"


class BadAccount:
    """Anti-pattern kept for teaching: the default list is created ONCE at def time."""

    def __init__(self, owner: str, transactions: list[int] = []) -> None:  # noqa: B006
        self.owner = owner
        self.transactions = transactions


@dataclass
class SavingsGoal:
    name: str
    target: Decimal
    saved: Decimal = Decimal("0")
    contributions: list[Decimal] = field(default_factory=list)
    progress: float = field(init=False)

    def __post_init__(self) -> None:
        """Runs after the generated ``__init__`` – validation and derived fields."""
        if self.target <= 0:
            raise ValueError("target must be positive")
        if not Decimal("0") <= self.saved <= self.target:
            raise ValueError("saved must be between 0 and target")
        self.progress = float(self.saved / self.target)


def main() -> None:
    print("Day 32 – Opening accounts\n")
    alice = BankAccount("  Alice   Smith ", Decimal("250"))
    bob = BankAccount("Bob", account_type="current")
    alice.withdraw(Decimal("50"))
    print(alice, bob, sep="\n")
    for bad in [("", Decimal("1")), ("Eve", Decimal("-5"))]:
        try:
            BankAccount(*bad)
        except ValueError as exc:
            print(f"Rejected {bad[0]!r}: {exc}")
    one, two = BadAccount("x"), BadAccount("y")
    one.transactions.append(99)
    print("Mutable default trap – second object sees:", two.transactions)
    print(SavingsGoal("bike", Decimal("400"), Decimal("100")))


if __name__ == "__main__":
    main()
