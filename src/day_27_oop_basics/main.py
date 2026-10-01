"""Day 27 – Python Object-Oriented Programming.

Scenario: a *payment gateway* that accepts several payment methods through one
abstract interface while hiding sensitive card data.

Deliverables (syllabus):
* OOP fundamentals: classes and objects
* Encapsulation (protected ``_attr``, name-mangled ``__attr``, read-only properties)
* Abstraction (``abc.ABC`` with ``@abstractmethod``)
* Polymorphism through a shared interface
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

DELIVERABLES: dict[str, str] = {
    "classes and objects": "Wallet",
    "encapsulation": "CreditCard",
    "abstraction": "PaymentMethod",
    "polymorphism": "checkout",
}


class PaymentDeclined(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Receipt:
    method: str
    amount: Decimal
    reference: str


class PaymentMethod(ABC):
    """Abstract base class: defines *what* every method can do, not *how*."""

    def __init__(self, owner: str) -> None:
        self._owner = owner  # protected by convention

    @property
    def owner(self) -> str:
        return self._owner

    @abstractmethod
    def authorize(self, amount: Decimal) -> str:
        """Charge *amount* and return a reference, or raise ``PaymentDeclined``."""

    @abstractmethod
    def describe(self) -> str: ...

    def pay(self, amount: Decimal) -> Receipt:
        """Template method: validation is shared, authorisation is subclass-specific."""
        if amount <= 0:
            raise ValueError("amount must be positive")
        return Receipt(self.describe(), amount, self.authorize(amount))


class CreditCard(PaymentMethod):
    def __init__(self, owner: str, number: str, limit: Decimal) -> None:
        super().__init__(owner)
        digits = number.replace(" ", "")
        if not (digits.isdigit() and 12 <= len(digits) <= 19):
            raise ValueError("invalid card number")
        self.__number = digits  # name-mangled to _CreditCard__number
        self.__limit = limit
        self._spent = Decimal("0")

    @property
    def masked_number(self) -> str:
        return "•••• " + self.__number[-4:]

    @property
    def available(self) -> Decimal:
        return self.__limit - self._spent

    def authorize(self, amount: Decimal) -> str:
        if amount > self.available:
            raise PaymentDeclined("credit limit exceeded")
        self._spent += amount
        return f"CC-{self.__number[-4:]}-{int(self._spent * 100)}"

    def describe(self) -> str:
        return f"Card {self.masked_number}"

    def __repr__(self) -> str:  # never leak the full number in logs
        return f"CreditCard(owner={self.owner!r}, number={self.masked_number!r})"


class Wallet(PaymentMethod):
    def __init__(self, owner: str, balance: Decimal = Decimal("0")) -> None:
        super().__init__(owner)
        self._balance = balance

    @property
    def balance(self) -> Decimal:  # read-only from outside: no setter
        return self._balance

    def top_up(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("top-up must be positive")
        self._balance += amount

    def authorize(self, amount: Decimal) -> str:
        if amount > self._balance:
            raise PaymentDeclined("insufficient wallet balance")
        self._balance -= amount
        return f"WL-{self.owner[:3].upper()}-{self._balance}"

    def describe(self) -> str:
        return f"Wallet of {self.owner}"


def checkout(method: PaymentMethod, amount: Decimal) -> str:
    """Works with *any* PaymentMethod – the caller never checks the concrete type."""
    try:
        receipt = method.pay(amount)
    except PaymentDeclined as exc:
        return f"declined ({exc})"
    return f"paid {receipt.amount} via {receipt.method}"


def main() -> None:
    print("Day 27 – Payment gateway\n")
    card = CreditCard("Ada", "4111 1111 1111 1111", Decimal("100"))
    wallet = Wallet("Grace", Decimal("20"))
    for method, amount in [(card, Decimal("60")), (wallet, Decimal("25")), (card, Decimal("50"))]:
        print(checkout(method, amount))
    print("repr hides the number:", repr(card))
    try:
        PaymentMethod("x")  # type: ignore[abstract]
    except TypeError as exc:
        print("Abstract class:", exc)


if __name__ == "__main__":
    main()
