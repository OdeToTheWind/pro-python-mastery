"""Day 36 – Python Instances and State.

Scenario: *food-delivery orders*. Every order object tracks its own state as
it moves through a lifecycle (placed → cooking → out for delivery → delivered,
or cancelled), records history, and releases resources when it closes.

Deliverables (syllabus):
* Instance variables (independent per object) vs class variables
* State tracking (a guarded state machine with history)
* Object lifecycle patterns (creation, transitions, snapshot/restore,
  context-managed close, finalizers)
"""

from __future__ import annotations

import itertools
import weakref
from dataclasses import dataclass
from datetime import datetime
from types import TracebackType
from typing import ClassVar, Self

DELIVERABLES: dict[str, str] = {
    "instance variables": "Order.__init__",
    "class variables": "Order.open_orders",
    "state tracking with allowed transitions": "Order.advance",
    "history of state changes": "Order.advance",
    "snapshot / restore": "Order.snapshot",
    "lifecycle: context manager and close": "Order.__exit__",
    "lifecycle: finalizer on garbage collection": "Order.__init__",
}

TRANSITIONS: dict[str, set[str]] = {
    "placed": {"cooking", "cancelled"},
    "cooking": {"out_for_delivery", "cancelled"},
    "out_for_delivery": {"delivered"},
    "delivered": set(),
    "cancelled": set(),
}


class InvalidTransition(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Snapshot:
    order_id: int
    state: str
    items: tuple[str, ...]


class Order:
    _ids: ClassVar[itertools.count[int]] = itertools.count(1)
    open_orders: ClassVar[int] = 0  # class variable: shared counter across all orders
    finalized: ClassVar[list[int]] = []

    def __init__(self, customer: str, items: list[str]) -> None:
        if not items:
            raise ValueError("an order needs at least one item")
        self.id = next(Order._ids)  # instance variables: unique per object
        self.customer = customer
        self.items = list(items)
        self.state = "placed"
        self.history: list[tuple[str, str]] = [("placed", "created")]
        self.closed = False
        Order.open_orders += 1
        # finalizer: runs when the object is garbage-collected (or at exit)
        weakref.finalize(self, Order.finalized.append, self.id)

    def advance(self, new_state: str, note: str = "") -> None:
        if self.closed:
            raise InvalidTransition(f"order {self.id} is closed")
        if new_state not in TRANSITIONS[self.state]:
            raise InvalidTransition(f"cannot go from {self.state} to {new_state}")
        self.state = new_state
        self.history.append((new_state, note or datetime.now().strftime("%H:%M")))

    @property
    def is_final(self) -> bool:
        return not TRANSITIONS[self.state]

    def snapshot(self) -> Snapshot:
        return Snapshot(self.id, self.state, tuple(self.items))

    def restore(self, snap: Snapshot) -> None:
        if snap.order_id != self.id:
            raise ValueError("snapshot belongs to another order")
        self.state, self.items = snap.state, list(snap.items)
        self.history.append((snap.state, "restored"))

    def close(self) -> None:
        if not self.closed:
            self.closed = True
            Order.open_orders -= 1

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc: BaseException | None,
                 tb: TracebackType | None) -> None:
        if exc_type is not None and not self.is_final:
            self.state = "cancelled"
            self.history.append(("cancelled", f"error: {exc}"))
        self.close()


def main() -> None:
    print("Day 36 – Delivery order lifecycle\n")
    with Order("Ana", ["pizza", "salad"]) as order:
        for step in ("cooking", "out_for_delivery", "delivered"):
            order.advance(step, note=step.replace("_", " "))
    other = Order("Ben", ["ramen"])
    print(f"order {order.id}: {order.state}; history {order.history}")
    print(f"order {other.id}: {other.state}; open orders: {Order.open_orders}")
    try:
        other.advance("delivered")
    except InvalidTransition as exc:
        print("Refused:", exc)
    try:
        with other:
            other.advance("cooking")
            raise RuntimeError("kitchen fire")
    except RuntimeError:
        pass
    print(f"after error: {other.state}; open orders: {Order.open_orders}")


if __name__ == "__main__":
    main()
