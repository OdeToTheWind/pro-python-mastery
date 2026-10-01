"""Day 09 – Logical Operations.

Scenario: an *office building access controller* deciding who may open which
door, and a tracer that proves when Python stops evaluating.

Deliverables (syllabus):
* ``and``, ``or``, ``not``
* Short-circuit evaluation
* Combining comparisons
* Access control
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from itertools import product

DELIVERABLES: dict[str, str] = {
    "and / or / not truth table": "truth_table",
    "short-circuit evaluation": "ShortCircuitTracer",
    "or/and return operands (not just bools)": "display_name",
    "combining comparisons": "within_hours",
    "access control": "can_open",
}

OFFICE_HOURS = (8, 19)


def truth_table() -> list[tuple[bool, bool, bool, bool, bool]]:
    """Rows of (A, B, A and B, A or B, not A)."""
    return [(a, b, a and b, a or b, not a) for a, b in product((False, True), repeat=2)]


def within_hours(hour: int, start: int = OFFICE_HOURS[0], end: int = OFFICE_HOURS[1]) -> bool:
    """Combine comparisons: ``0 <= hour <= 23 and start <= hour < end``."""
    return 0 <= hour <= 23 and start <= hour < end


def can_open(door: str, *, role: str, has_badge: bool, hour: int, escorted: bool = False) -> bool:
    """Decide door access by combining ``and``/``or``/``not``.

    * lobby: anyone during office hours, staff with a badge at any time
    * lab: staff with a badge, or a visitor who is escorted during office hours
    * server room: admins with a badge only, never visitors
    """
    is_staff = role in {"staff", "admin"}
    if is_staff and not has_badge and door != "lobby":
        return False  # `not`: a staff member without a badge is treated like a stranger
    if door == "lobby":
        return within_hours(hour) or (is_staff and has_badge)
    if door == "lab":
        return (is_staff and has_badge) or (role == "visitor" and escorted and within_hours(hour))
    if door == "server_room":
        return role == "admin" and has_badge
    raise ValueError(f"unknown door {door!r}")


@dataclass
class ShortCircuitTracer:
    """Records which operands were evaluated, proving short-circuiting."""

    calls: list[str] = field(default_factory=list)

    def check(self, name: str, result: bool) -> Callable[[], bool]:
        def operand() -> bool:
            self.calls.append(name)
            return result

        return operand

    def evaluate_and(self, left: bool, right: bool) -> bool:
        self.calls.clear()
        return self.check("left", left)() and self.check("right", right)()

    def evaluate_or(self, left: bool, right: bool) -> bool:
        self.calls.clear()
        return self.check("left", left)() or self.check("right", right)()


def display_name(nickname: str | None, full_name: str | None) -> str:
    """``or`` returns the first truthy *operand* – handy for defaults."""
    return nickname or full_name or "Guest"


def safe_ratio(granted: int, attempts: int) -> float:
    """``and`` guards the division: if attempts is 0 the right side never runs."""
    return attempts != 0 and granted / attempts or 0.0


def main() -> None:
    print("Day 09 – Logical operations\n")
    print(" A      B      and    or     not A")
    for row in truth_table():
        print(" ".join(f"{value!s:<6}" for value in row))

    tracer = ShortCircuitTracer()
    tracer.evaluate_and(False, True)
    print(f"\nFalse and ... evaluated: {tracer.calls}")
    tracer.evaluate_or(True, False)
    print(f"True or ... evaluated:   {tracer.calls}")

    print("\nAccess decisions:")
    scenarios = [
        ("lobby", "visitor", False, 22, False),
        ("lobby", "staff", True, 22, False),
        ("lab", "visitor", False, 10, True),
        ("server_room", "staff", True, 10, False),
        ("server_room", "admin", True, 3, False),
    ]
    for door, role, badge, hour, escorted in scenarios:
        allowed = can_open(door, role=role, has_badge=badge, hour=hour, escorted=escorted)
        print(f"  {role:<8} → {door:<12} at {hour:02d}:00 : {'OPEN' if allowed else 'DENIED'}")
    print(f"\nWelcome, {display_name('', None)}! Success ratio: {safe_ratio(0, 0)}")


if __name__ == "__main__":
    main()
