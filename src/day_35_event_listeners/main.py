"""Day 35 – Event Listeners.

Scenario: a *smart-home hub*. Devices emit events (doorbell rang, motion
detected); any number of independent listeners react without the devices
knowing who is listening.

Deliverables (syllabus):
* Event-driven patterns (publish/subscribe, decoupling)
* Callback-based interactions (register, unregister, once, decorator registration)
"""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

DELIVERABLES: dict[str, str] = {
    "event-driven pattern (publish/subscribe)": "EventBus",
    "callbacks": "EventBus.on",
    "unsubscribe": "EventBus.off",
    "one-shot listeners": "EventBus.once",
    "decorator registration": "EventBus.listener",
    "error isolation between listeners": "EventBus.emit",
    "devices that emit events": "Doorbell",
}

Callback = Callable[..., Any]


@dataclass
class EventBus:
    _listeners: dict[str, list[tuple[int, Callback]]] = field(default_factory=lambda: defaultdict(list))
    errors: list[str] = field(default_factory=list)

    def on(self, event: str, callback: Callback, *, priority: int = 0) -> Callable[[], None]:
        """Register *callback*; higher priority runs first. Returns an unsubscribe function."""
        self._listeners[event].append((priority, callback))
        self._listeners[event].sort(key=lambda pair: -pair[0])

        def unsubscribe() -> None:
            self.off(event, callback)

        return unsubscribe

    def off(self, event: str, callback: Callback) -> bool:
        before = len(self._listeners[event])
        self._listeners[event] = [(p, cb) for p, cb in self._listeners[event] if cb is not callback]
        return len(self._listeners[event]) < before

    def once(self, event: str, callback: Callback) -> None:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.off(event, wrapper)
            return callback(*args, **kwargs)

        self.on(event, wrapper)

    def listener(self, event: str, *, priority: int = 0) -> Callable[[Callback], Callback]:
        """Decorator form: ``@bus.listener("doorbell")``."""

        def register(callback: Callback) -> Callback:
            self.on(event, callback, priority=priority)
            return callback

        return register

    def emit(self, event: str, **payload: Any) -> list[Any]:
        """Call every listener; one failing listener must not stop the others."""
        results = []
        for _, callback in list(self._listeners[event]):
            try:
                results.append(callback(**payload))
            except Exception as exc:  # noqa: BLE001 – isolate faulty listeners
                self.errors.append(f"{event}: {getattr(callback, '__name__', callback)} failed: {exc}")
        return results

    def listener_count(self, event: str) -> int:
        return len(self._listeners[event])


class Doorbell:
    """A device that only knows the bus, not who listens."""

    def __init__(self, bus: EventBus, location: str) -> None:
        self.bus, self.location = bus, location

    def press(self, visitor: str) -> list[Any]:
        return self.bus.emit("doorbell", location=self.location, visitor=visitor)


def build_home(log: list[str]) -> tuple[EventBus, Doorbell]:
    bus = EventBus()

    @bus.listener("doorbell", priority=10)
    def turn_on_porch_light(location: str, visitor: str) -> str:
        log.append(f"light on at {location}")
        return "light"

    def notify_phone(location: str, visitor: str) -> str:
        log.append(f"phone: {visitor} is at the {location}")
        return "phone"

    bus.on("doorbell", notify_phone)
    def award_first_visitor_badge(location: str, visitor: str) -> str:
        log.append("first-visitor badge")
        return "badge"

    bus.once("doorbell", award_first_visitor_badge)
    return bus, Doorbell(bus, "front door")


def main() -> None:
    log: list[str] = []
    bus, bell = build_home(log)
    print("Day 35 – Smart-home event hub\n")
    print("1st press →", bell.press("courier"))
    print("2nd press →", bell.press("neighbour"))
    unsubscribe = bus.on("doorbell", lambda **_: 1 / 0)
    print("faulty listener added →", bell.press("friend"), "| errors:", bus.errors)
    unsubscribe()
    print("Log:", log)


if __name__ == "__main__":
    main()
