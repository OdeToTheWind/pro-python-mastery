"""Day 01 – Variables, Type Hinting & Scoping.

Scenario: a *learning-streak tracker* that records study sessions.

Deliverables (syllabus):
* Strict typing with PEP 484 annotations and PEP 695 ``type`` aliases / generics
* f-strings with format specifications
* Scope rules: local vs global vs nonlocal
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

# --- PEP 695: type aliases and generic functions (Python 3.12+) -------------
type Minutes = int
type SessionLog = list[tuple[str, Minutes]]

DELIVERABLES: dict[str, str] = {
    "PEP 484 annotations": "format_status",
    "PEP 695 type alias + generic function": "first_or_default",
    "f-strings with format specs": "format_status",
    "global scope (global keyword)": "record_session",
    "enclosing scope (nonlocal keyword)": "make_streak_counter",
    "local scope shadowing a global": "shadowing_demo",
}

# Module-level (global) state. Functions must opt in with ``global`` to rebind it.
total_minutes: Minutes = 0
label: str = "global label"


def first_or_default[T](items: Sequence[T], default: T) -> T:
    """Return the first item of *items*, or *default* when it is empty.

    ``[T]`` declares a type parameter (PEP 695), so the return type follows
    whatever sequence type the caller passes in.
    """
    return items[0] if items else default


def format_status(name: str, day: int, minutes: Minutes, active: bool) -> str:
    """Build a one-line status using f-string format specifications.

    ``:<12`` left-aligns, ``:03d`` zero-pads, ``:>5,`` right-aligns with a
    thousands separator and ``!r`` shows the ``repr``.
    """
    state = "active" if active else "paused"
    return f"{name:<12}| day {day:03d} | {minutes:>5,} min | {state!r}"


def record_session(minutes: Minutes) -> Minutes:
    """Add *minutes* to the module-level total and return the new total.

    Without ``global`` the assignment would create a new *local* variable and
    ``total_minutes += minutes`` would raise ``UnboundLocalError``.
    """
    global total_minutes
    if minutes < 0:
        raise ValueError("minutes cannot be negative")
    total_minutes += minutes
    return total_minutes


def reset_sessions() -> None:
    """Reset the global total (used by the demo and the tests)."""
    global total_minutes
    total_minutes = 0


def make_streak_counter() -> Callable[[bool], int]:
    """Return a closure that tracks a consecutive-day streak.

    ``streak`` lives in the *enclosing* function's scope; the inner function
    rebinds it with ``nonlocal``.
    """
    streak = 0

    def studied_today(did_study: bool) -> int:
        nonlocal streak
        streak = streak + 1 if did_study else 0
        return streak

    return studied_today


def shadowing_demo() -> tuple[str, str]:
    """Show that a local name hides the global one only inside the function."""
    label = "local label"  # noqa: F841 – intentionally shadows the global
    inside = label
    return inside, globals()["label"]


def summarize(log: SessionLog) -> str:
    """Summarise a session log, using the generic helper and f-strings."""
    first_topic, _ = first_or_default(log, ("nothing yet", 0))
    total = sum(minutes for _, minutes in log)
    return f"{len(log)} sessions, {total / 60:.1f} h total, first topic: {first_topic}"


def main() -> None:
    reset_sessions()
    log: SessionLog = [("typing", 45), ("f-strings", 30), ("scope", 50)]
    print("Day 01 – Variables, Type Hinting & Scoping\n")
    for topic, minutes in log:
        record_session(minutes)
        print(format_status(topic, 1, minutes, active=True))
    print(f"\nGlobal total after record_session(): {total_minutes} min")

    counter = make_streak_counter()
    streaks = [counter(day) for day in (True, True, False, True)]
    print(f"Streak values with nonlocal closure: {streaks}")

    inside, outside = shadowing_demo()
    print(f"Inside function: {inside!r} | module global: {outside!r}")
    print(summarize(log))


if __name__ == "__main__":
    main()
