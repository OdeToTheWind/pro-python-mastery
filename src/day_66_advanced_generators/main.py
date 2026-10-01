"""Day 66 – Advanced Generators.

Scenario: an *online-shop order pipeline* – raw order lines flow through
composable generator stages (parse → validate → enrich → batch), nested
category trees are flattened with ``yield from``, and a live revenue tracker
receives values via ``send()``.

Deliverables (syllabus):
* ``yield from`` (delegation, flattening, capturing a sub-generator's return value)
* Generator pipelines (stages chained lazily)
* Sending values (``send``, priming, ``throw`` and ``close``)
"""

from __future__ import annotations

from collections.abc import Generator, Iterable, Iterator
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any

DELIVERABLES: dict[str, str] = {
    "yield from: flattening nested data": "walk_categories",
    "yield from: capturing a return value": "count_and_forward",
    "pipeline stage: parse": "parse_lines",
    "pipeline stage: validate": "valid_orders",
    "pipeline stage: enrich": "with_tax",
    "pipeline stage: batch": "batched",
    "composed pipeline": "build_pipeline",
    "send() into a coroutine-style generator": "revenue_tracker",
    "throw() and close()": "revenue_tracker",
}


@dataclass(frozen=True, slots=True)
class Order:
    order_id: str
    sku: str
    quantity: int
    unit_price: Decimal
    country: str


VAT = {"DE": Decimal("0.19"), "FR": Decimal("0.20"), "IN": Decimal("0.18")}


def walk_categories(tree: dict[str, Any], prefix: str = "") -> Iterator[str]:
    """Recursively yield "Parent/Child" paths – ``yield from`` delegates to the recursion."""
    for name, children in tree.items():
        path = f"{prefix}/{name}" if prefix else name
        yield path
        if children:
            yield from walk_categories(children, path)


def parse_lines(lines: Iterable[str]) -> Iterator[dict[str, str]]:
    for line in lines:
        if not line.strip() or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) != 5:
            continue
        yield dict(zip(("order_id", "sku", "quantity", "unit_price", "country"), parts, strict=True))


def valid_orders(rows: Iterable[dict[str, str]], rejected: list[str]) -> Iterator[Order]:
    for row in rows:
        try:
            order = Order(row["order_id"], row["sku"], int(row["quantity"]),
                          Decimal(row["unit_price"]), row["country"].upper())
        except (ValueError, InvalidOperation):
            rejected.append(row["order_id"])
            continue
        if order.quantity <= 0 or order.country not in VAT:
            rejected.append(order.order_id)
            continue
        yield order


def with_tax(orders: Iterable[Order]) -> Iterator[tuple[Order, Decimal]]:
    for order in orders:
        gross = order.quantity * order.unit_price * (1 + VAT[order.country])
        yield order, gross.quantize(Decimal("0.01"))


def batched[T](items: Iterable[T], size: int) -> Iterator[list[T]]:
    if size < 1:
        raise ValueError("batch size must be positive")
    batch: list[T] = []
    for item in items:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


def build_pipeline(lines: Iterable[str], rejected: list[str], batch_size: int = 2) -> Iterator[list[tuple[Order, Decimal]]]:
    """Each stage pulls from the previous one – nothing runs until iteration starts."""
    return batched(with_tax(valid_orders(parse_lines(lines), rejected)), batch_size)


def _forward(items: Iterable[str]) -> Generator[str, None, int]:
    count = 0
    for item in items:
        count += 1
        yield item
    return count  # becomes StopIteration.value


def count_and_forward(items: Iterable[str], totals: list[int]) -> Iterator[str]:
    """``result = yield from sub()`` re-yields everything *and* captures the return value."""
    total = yield from _forward(items)
    totals.append(total)


def revenue_tracker() -> Generator[dict[str, Decimal | int], Decimal | None, Decimal]:
    """Receives sale amounts via ``send()``; yields running statistics.

    * ``throw(ValueError)`` reports a refund-reversal error without killing the tracker
    * ``close()`` (or sending ``None``) finishes; the total is the return value
    """
    total, count = Decimal("0"), 0
    stats: dict[str, Decimal | int] = {"total": total, "count": count, "average": Decimal("0")}
    while True:
        try:
            amount = yield stats
        except ValueError:
            stats = {**stats, "errors": int(stats.get("errors", 0)) + 1}
            continue
        if amount is None:
            return total
        total += amount
        count += 1
        stats = {**stats, "total": total, "count": count,
                 "average": (total / count).quantize(Decimal("0.01"))}


RAW = [
    "# order_id, sku, qty, price, country",
    "A1, MUG-01, 2, 12.50, DE",
    "A2, TEE-07, 1, 19.99, fr",
    "A3, MUG-01, zero, 12.50, DE",
    "A4, CAP-02, 3, 9.00, US",
    "A5, TEE-07, 4, 19.99, IN",
    "broken line",
]


def main() -> None:
    print("Day 66 – Order pipeline\n")
    rejected: list[str] = []
    for batch in build_pipeline(RAW, rejected):
        print("batch:", [(order.order_id, str(gross)) for order, gross in batch])
    print("rejected:", rejected)
    tree = {"Clothing": {"Shirts": {}, "Hats": {"Caps": {}}}, "Kitchen": {"Mugs": {}}}
    print("categories:", list(walk_categories(tree)))
    totals: list[int] = []
    print("forwarded:", list(count_and_forward(["x", "y", "z"], totals)), "count returned:", totals)
    tracker = revenue_tracker()
    next(tracker)  # prime: run to the first yield
    for amount in ("25.00", "40.00", "10.50"):
        print("send", amount, "→", tracker.send(Decimal(amount)))
    print("after throw:", tracker.throw(ValueError("bad refund")))
    tracker.close()


if __name__ == "__main__":
    main()
