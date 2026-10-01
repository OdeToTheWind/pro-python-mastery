"""Day 47 – Packing and Unpacking Functions in Python.

Scenario: a *GPS route planner* – coordinates, waypoints and connection
settings are passed around as tuples and dicts, then unpacked straight into
function calls.

Deliverables (syllabus):
* Advanced argument unpacking with ``*`` (sequences → positional arguments)
* Advanced argument unpacking with ``**`` (mappings → keyword arguments)
* Packing (``*args``/``**kwargs``), extended unpacking (``first, *rest``),
  merging with ``[*a, *b]`` / ``{**a, **b}``, and ``zip(*pairs)``
"""

from __future__ import annotations

import math
from typing import Any

DELIVERABLES: dict[str, str] = {
    "* unpacking at the call site": "leg_distance",
    "** unpacking at the call site": "connect",
    "packing with *args": "route_length",
    "packing with **kwargs": "connect",
    "extended unpacking (first, *middle, last)": "split_route",
    "merging with [*a, *b] and {**a, **b}": "merge_settings",
    "unzipping with zip(*pairs)": "unzip",
    "swap via tuple packing/unpacking": "swap_ends",
}

Point = tuple[float, float]
DEFAULT_SETTINGS = {"host": "maps.example.com", "port": 443, "timeout": 5.0}


def leg_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in km (haversine). Takes four separate numbers."""
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return round(2 * r * math.asin(math.sqrt(a)), 1)


def route_length(*points: Point) -> float:
    """``*points`` *packs* any number of tuples; ``*a, *b`` *unpacks* two of them."""
    return round(sum(leg_distance(*a, *b) for a, b in zip(points, points[1:], strict=False)), 1)


def connect(host: str, port: int, *, timeout: float = 10.0, **extra: Any) -> str:
    """Accepts a settings dict via ``connect(**settings)``; unknown keys land in ``extra``."""
    options = ", ".join(f"{k}={v}" for k, v in sorted(extra.items()))
    return f"{host}:{port} (timeout {timeout}s{', ' + options if options else ''})"


def split_route(route: list[str]) -> tuple[str, list[str], str]:
    """Extended unpacking: start, any number of stops, destination."""
    if len(route) < 2:
        raise ValueError("a route needs a start and a destination")
    start, *stops, destination = route
    return start, stops, destination


def merge_settings(*overrides: dict[str, Any]) -> dict[str, Any]:
    """``{**a, **b}``: later dictionaries win."""
    merged: dict[str, Any] = {**DEFAULT_SETTINGS}
    for override in overrides:
        merged = {**merged, **override}
    return merged


def join_routes(first: list[str], second: list[str]) -> list[str]:
    """``[*a, *b]`` – and skip the shared stop where they meet."""
    tail = second[1:] if first and second and first[-1] == second[0] else second
    return [*first, *tail]


def unzip(pairs: list[tuple[str, float]]) -> tuple[tuple[str, ...], tuple[float, ...]]:
    """``zip(*pairs)`` transposes a list of pairs into two tuples."""
    if not pairs:
        return (), ()
    names, values = zip(*pairs, strict=True)
    return names, values


def swap_ends(route: list[str]) -> list[str]:
    result = list(route)
    result[0], result[-1] = result[-1], result[0]  # pack right side, unpack into left
    return result


def main() -> None:
    london, paris, berlin = (51.5074, -0.1278), (48.8566, 2.3522), (52.52, 13.405)
    print("Day 47 – Route planner\n")
    print("London → Paris:", leg_distance(*london, *paris), "km")
    print("London → Paris → Berlin:", route_length(london, paris, berlin), "km")
    settings = merge_settings({"timeout": 2.5}, {"retries": 3, "region": "eu"})
    print("connect(**settings):", connect(**settings))
    start, stops, end = split_route(["Home", "Café", "Library", "Gym", "Office"])
    print(f"start={start} stops={stops} end={end}")
    print("joined:", join_routes(["A", "B"], ["B", "C", "D"]))
    print("unzipped:", unzip([("A", 1.2), ("B", 3.4)]))


if __name__ == "__main__":
    main()
