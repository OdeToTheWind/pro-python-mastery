"""Day 12 – Functions.

Scenario: a *coffee-shop ordering system* built from small, documented,
type-hinted functions.

Deliverables (syllabus):
* Parameters and default arguments
* ``*args`` and ``**kwargs``
* Docstrings
* Type hints
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

DELIVERABLES: dict[str, str] = {
    "parameters": "price_drink",
    "default arguments": "price_drink",
    "*args": "order_total",
    "**kwargs": "customize",
    "docstrings": "price_drink",
    "type hints": "Drink",
}

MENU: dict[str, Decimal] = {"espresso": Decimal("2.20"), "latte": Decimal("3.40"),
                            "tea": Decimal("1.90")}
SIZE_MULTIPLIER: dict[str, Decimal] = {"small": Decimal("0.8"), "medium": Decimal("1"),
                                       "large": Decimal("1.3")}
EXTRA_PRICES: dict[str, Decimal] = {"oat_milk": Decimal("0.40"), "extra_shot": Decimal("0.60"),
                                    "syrup": Decimal("0.35")}


@dataclass(frozen=True, slots=True)
class Drink:
    name: str
    size: str
    price: Decimal
    extras: dict[str, int] = field(default_factory=dict)


def price_drink(name: str, size: str = "medium") -> Decimal:
    """Return the price of a drink.

    Args:
        name: Menu item, e.g. ``"latte"``.
        size: ``"small"``, ``"medium"`` (default) or ``"large"``.

    Returns:
        The price rounded to cents.

    Raises:
        KeyError: If the drink or size is not on the menu.
    """
    return (MENU[name] * SIZE_MULTIPLIER[size]).quantize(Decimal("0.01"))


def customize(name: str, size: str = "medium", **extras: int) -> Drink:
    """Build a drink with any number of keyword extras, e.g. ``extra_shot=2``.

    ``**extras`` collects unknown keyword arguments into a ``dict``.
    """
    unknown = set(extras) - set(EXTRA_PRICES)
    if unknown:
        raise ValueError(f"unknown extras: {', '.join(sorted(unknown))}")
    if any(qty < 0 for qty in extras.values()):
        raise ValueError("extra quantities cannot be negative")
    price = price_drink(name, size) + sum(
        (EXTRA_PRICES[extra] * qty for extra, qty in extras.items()), Decimal("0")
    )
    return Drink(name, size, price, dict(extras))


def order_total(*drinks: Drink, tip_percent: int = 0) -> Decimal:
    """Sum any number of drinks (``*drinks`` is a tuple) and add an optional tip."""
    subtotal = sum((drink.price for drink in drinks), Decimal("0"))
    return (subtotal * (100 + tip_percent) / 100).quantize(Decimal("0.01"))


def receipt_line(drink: Drink) -> str:
    """One aligned receipt line for *drink*."""
    extras = ", ".join(f"{k}×{v}" for k, v in drink.extras.items() if v)
    label = f"{drink.size} {drink.name}" + (f" ({extras})" if extras else "")
    return f"{label:<38}€{drink.price:>6}"


def main() -> None:
    print("Day 12 – Coffee shop orders\n")
    order = [
        customize("latte", "large", oat_milk=1, extra_shot=1),
        customize("espresso"),
        customize("tea", size="small", syrup=2),
    ]
    for drink in order:
        print(receipt_line(drink))
    print(f"{'Total incl. 10% tip':<38}€{order_total(*order, tip_percent=10):>6}")
    print("\nDocstring of price_drink():\n" + (price_drink.__doc__ or "").split("\n\n")[0])


if __name__ == "__main__":
    main()
