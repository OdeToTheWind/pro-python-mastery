"""Day 18 – Python Dictionaries and Lists.

Scenario: a *neighbourhood grocery store* – a dict-based inventory behind the
counter and a list-based shopping cart in front of it.

Deliverables (syllabus):
* List methods (append, extend, insert, remove, pop, sort, count, index)
* Dict methods (get, setdefault, update, pop, items, keys, values)
* Inventory management
* Shopping-cart logic
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

DELIVERABLES: dict[str, str] = {
    "list methods": "list_method_tour",
    "dict methods": "Inventory",
    "inventory management": "Inventory",
    "shopping cart logic": "Cart",
}


class OutOfStockError(Exception):
    """Raised when the cart asks for more than the store holds."""


@dataclass
class Inventory:
    """Stock levels and prices keyed by product name (a dict of dicts)."""

    stock: dict[str, int] = field(default_factory=dict)
    prices: dict[str, Decimal] = field(default_factory=dict)

    def add_product(self, name: str, price: str, quantity: int = 0) -> None:
        if quantity < 0:
            raise ValueError("quantity cannot be negative")
        self.prices[name] = Decimal(price)
        self.stock[name] = self.stock.get(name, 0) + quantity  # .get with default

    def restock(self, deliveries: dict[str, int]) -> None:
        """Add several deliveries at once; unknown products are rejected."""
        unknown = deliveries.keys() - self.prices.keys()
        if unknown:
            raise KeyError(f"unknown products: {sorted(unknown)}")
        for name, qty in deliveries.items():
            if qty < 0:
                raise ValueError("delivery quantities cannot be negative")
            self.stock[name] += qty

    def take(self, name: str, quantity: int) -> None:
        available = self.stock.get(name, 0)
        if quantity > available:
            raise OutOfStockError(f"only {available} × {name} left")
        self.stock[name] = available - quantity

    def discontinue(self, name: str) -> int:
        """Remove a product with ``dict.pop`` and return the stock that was left."""
        self.prices.pop(name)
        return self.stock.pop(name, 0)

    def low_stock(self, threshold: int = 5) -> list[str]:
        return sorted(name for name, qty in self.stock.items() if qty <= threshold)

    def value(self) -> Decimal:
        return sum((self.prices[n] * q for n, q in self.stock.items()), Decimal("0"))


@dataclass
class Cart:
    """An ordered list of ``(product, quantity)`` lines."""

    inventory: Inventory
    lines: list[tuple[str, int]] = field(default_factory=list)

    def add(self, name: str, quantity: int = 1) -> None:
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if name not in self.inventory.prices:
            raise KeyError(name)
        in_cart = sum(q for n, q in self.lines if n == name)
        if in_cart + quantity > self.inventory.stock.get(name, 0):
            raise OutOfStockError(f"not enough {name}")
        self.lines.append((name, quantity))

    def remove(self, name: str) -> None:
        """Remove every line for *name* (list comprehension rebuild)."""
        if all(n != name for n, _ in self.lines):
            raise ValueError(f"{name} is not in the cart")
        self.lines = [(n, q) for n, q in self.lines if n != name]

    def merged(self) -> dict[str, int]:
        totals: dict[str, int] = {}
        for name, qty in self.lines:
            totals[name] = totals.get(name, 0) + qty
        return totals

    def total(self) -> Decimal:
        return sum(
            (self.inventory.prices[n] * q for n, q in self.merged().items()), Decimal("0")
        )

    def checkout(self) -> Decimal:
        """Take stock for every line atomically: either all lines succeed or none."""
        merged = self.merged()
        for name, qty in merged.items():
            if qty > self.inventory.stock.get(name, 0):
                raise OutOfStockError(f"not enough {name}")
        for name, qty in merged.items():
            self.inventory.take(name, qty)
        amount = self.total()
        self.lines.clear()
        return amount


def list_method_tour() -> dict[str, object]:
    """Exercise the core list methods on a delivery manifest."""
    manifest = ["milk", "eggs", "bread"]
    manifest.append("apples")
    manifest.extend(["eggs", "rice"])
    manifest.insert(0, "coffee")
    manifest.remove("eggs")  # first occurrence only
    last = manifest.pop()
    manifest.sort()
    return {
        "manifest": manifest,
        "popped": last,
        "eggs count": manifest.count("eggs"),
        "bread index": manifest.index("bread"),
    }


def demo_store() -> Inventory:
    store = Inventory()
    for name, price, qty in [("milk", "1.10", 10), ("eggs", "0.30", 24), ("bread", "2.50", 3)]:
        store.add_product(name, price, qty)
    return store


def main() -> None:
    print("Day 18 – Grocery store\n")
    print("List tour:", list_method_tour())
    store = demo_store()
    cart = Cart(store)
    cart.add("milk", 2)
    cart.add("eggs", 12)
    cart.add("milk", 1)
    print("Cart lines:", cart.lines, "merged:", cart.merged())
    try:
        cart.add("bread", 5)
    except OutOfStockError as exc:
        print("Refused:", exc)
    print("Paid €", cart.checkout())
    store.restock({"bread": 10})
    print("Stock now:", store.stock, "| low stock:", store.low_stock(), "| value €", store.value())


if __name__ == "__main__":
    main()
