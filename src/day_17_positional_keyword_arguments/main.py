"""Day 17 – Positional and Keyword Arguments.

Scenario: an *airline booking API* where some arguments must be positional
(route), some must be named (cabin, flexibility) and some are optional.

Deliverables (syllabus):
* Positional vs keyword arguments (incl. positional-only ``/`` and keyword-only ``*``)
* Defaults
* Argument flexibility (``*args`` / ``**kwargs`` at the call boundary)
"""

from __future__ import annotations

import inspect
from collections.abc import Callable
from typing import Any

DELIVERABLES: dict[str, str] = {
    "positional arguments": "book_flight",
    "keyword arguments": "book_flight",
    "positional-only parameters (/)": "book_flight",
    "keyword-only parameters (*)": "book_flight",
    "default values": "book_flight",
    "argument flexibility (*names, **titles)": "boarding_announcement",
    "inspecting how arguments bind": "how_arguments_bind",
}

CABIN_MULTIPLIER = {"economy": 1.0, "premium": 1.6, "business": 3.2}


def book_flight(
    origin: str,
    destination: str,
    /,
    passengers: int = 1,
    *,
    cabin: str = "economy",
    flexible: bool = False,
    base_fare: float = 120.0,
) -> dict[str, Any]:
    """Book a flight.

    * ``origin``/``destination`` are **positional-only** (before ``/``) – callers
      can't write ``origin=`` so we may rename them later without breaking code.
    * ``passengers`` may be passed either way.
    * ``cabin``/``flexible``/``base_fare`` are **keyword-only** (after ``*``) –
      ``book_flight("LHR", "JFK", 2, "business")`` is a ``TypeError``, which
      prevents mixing up two string arguments.
    """
    if origin.upper() == destination.upper():
        raise ValueError("origin and destination must differ")
    if passengers < 1:
        raise ValueError("at least one passenger")
    if cabin not in CABIN_MULTIPLIER:
        raise ValueError(f"cabin must be one of {sorted(CABIN_MULTIPLIER)}")
    fare = base_fare * CABIN_MULTIPLIER[cabin] * passengers * (1.15 if flexible else 1.0)
    return {
        "route": f"{origin.upper()}→{destination.upper()}",
        "passengers": passengers,
        "cabin": cabin,
        "flexible": flexible,
        "total": round(fare, 2),
    }


def boarding_announcement(*names: str, greeting: str = "Welcome aboard", **titles: str) -> list[str]:
    """Greet any number of passengers; ``titles`` maps a lowercase name to a title.

    ``greeting`` sits *after* ``*names`` so it can only be given by keyword and
    is never swallowed by a passenger name.
    """
    lines = []
    for name in names:
        title = titles.get(name.lower())
        person = f"{title} {name}" if title else name
        lines.append(f"{greeting}, {person}!")
    return lines or [f"{greeting}, everyone!"]


def how_arguments_bind(func: Callable[..., Any], *args: Any, **kwargs: Any) -> dict[str, Any]:
    """Show which parameter each argument lands in (defaults included)."""
    bound = inspect.signature(func).bind(*args, **kwargs)
    bound.apply_defaults()
    return dict(bound.arguments)


def parameter_kinds(func: Callable[..., Any]) -> dict[str, str]:
    return {name: p.kind.description for name, p in inspect.signature(func).parameters.items()}


def main() -> None:
    print("Day 17 – Airline booking arguments\n")
    print(book_flight("lhr", "jfk"))
    print(book_flight("LHR", "JFK", 2, cabin="business", flexible=True))
    print("\nParameter kinds:", parameter_kinds(book_flight))
    print("Binding:", how_arguments_bind(book_flight, "DEL", "BLR", passengers=3))
    mistakes: dict[str, Callable[[], object]] = {
        'book_flight(origin="LHR", destination="JFK")':
            lambda: book_flight(origin="LHR", destination="JFK"),  # type: ignore[call-arg]
        'book_flight("LHR", "JFK", 2, "business")':
            lambda: book_flight("LHR", "JFK", 2, "business"),  # type: ignore[misc]
    }
    for label, call in mistakes.items():
        try:
            call()
        except TypeError as exc:
            print(f"TypeError for {label}: {exc}")
    print("\n".join(boarding_announcement("Aarav", "Diya", greeting="Namaste", diya="Dr.")))


if __name__ == "__main__":
    main()
