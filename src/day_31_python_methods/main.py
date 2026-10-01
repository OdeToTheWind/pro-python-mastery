"""Day 31 – Python Methods.

Scenario: a *pizzeria ordering system* where each kind of method has a clear
job: instance methods change one pizza, class methods build pizzas or change
shop-wide settings, static methods are utilities that need neither.

Deliverables (syllabus):
* Instance methods (``self``)
* Class methods (``cls``) – incl. alternative constructors
* Static methods
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from decimal import Decimal
from typing import Any, Self

DELIVERABLES: dict[str, str] = {
    "instance methods": "Pizza.add_topping",
    "class methods: alternative constructors": "Pizza.margherita",
    "class methods: shared class state": "Pizza.set_base_price",
    "static methods": "Pizza.valid_size",
}


class Pizza:
    base_price = Decimal("8.00")  # shared by all pizzas
    size_factor = {"small": Decimal("0.8"), "medium": Decimal("1"), "large": Decimal("1.25")}
    topping_price = Decimal("1.20")

    def __init__(self, size: str = "medium", toppings: list[str] | None = None) -> None:
        if not self.valid_size(size):
            raise ValueError(f"unknown size {size!r}")
        self.size = size
        self.toppings: list[str] = list(toppings or [])

    # ----- instance methods: operate on *this* pizza ----------------------
    def add_topping(self, topping: str) -> Self:
        topping = topping.strip().lower()
        if not topping:
            raise ValueError("topping name required")
        if topping in self.toppings:
            raise ValueError(f"{topping} already added")
        self.toppings.append(topping)
        return self  # enables chaining: pizza.add_topping("a").add_topping("b")

    def price(self) -> Decimal:
        base = type(self).base_price * self.size_factor[self.size]
        return (base + self.topping_price * len(self.toppings)).quantize(Decimal("0.01"))

    # ----- class methods: receive the class, not an instance --------------
    @classmethod
    def margherita(cls, size: str = "medium") -> Self:
        """Alternative constructor – returns ``cls(...)`` so subclasses get subclasses."""
        return cls(size, ["tomato", "mozzarella", "basil"])

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(data.get("size", "medium"), list(data.get("toppings", [])))

    @classmethod
    def set_base_price(cls, price: Decimal) -> None:
        if price <= 0:
            raise ValueError("base price must be positive")
        cls.base_price = price

    # ----- static methods: no self, no cls --------------------------------
    @staticmethod
    def valid_size(size: str) -> bool:
        return size in Pizza.size_factor

    @staticmethod
    def format_price(amount: Decimal) -> str:
        return f"€{amount:.2f}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.size!r}, {self.toppings!r})"


class GlutenFreePizza(Pizza):
    base_price = Decimal("9.50")


@contextmanager
def temporary_base_price(price: Decimal) -> Iterator[None]:
    """Change class-wide state and always restore it (useful in tests and promos)."""
    original = Pizza.base_price
    Pizza.set_base_price(price)
    try:
        yield
    finally:
        Pizza.base_price = original


def main() -> None:
    print("Day 31 – Pizzeria methods\n")
    order = [Pizza.margherita("large"), Pizza("small").add_topping("olives").add_topping("ham"),
             GlutenFreePizza.margherita(), Pizza.from_dict({"size": "medium", "toppings": ["corn"]})]
    for pizza in order:
        print(f"{pizza!r:<64} {Pizza.format_price(pizza.price())}")
    with temporary_base_price(Decimal("6.00")):
        print("Happy hour medium margherita:", Pizza.format_price(Pizza.margherita().price()))
    print("Valid size 'huge'?", Pizza.valid_size("huge"))


if __name__ == "__main__":
    main()
