"""Day 08 – If / Elif / Else Conditionals.

Scenario: a *hiking-trip weather advisor* that decides what to pack and
whether the hike is safe.

Deliverables (syllabus):
* Comparison operators (``== != < <= > >=``)
* Nested logic
* Truthy / falsy values
* Chained conditionals (``elif`` ladders and chained comparisons ``a <= x < b``)
"""

from __future__ import annotations

import math

DELIVERABLES: dict[str, str] = {
    "comparison operators": "compare",
    "chained comparisons and elif ladder": "classify_temperature",
    "nested logic": "hike_decision",
    "truthy/falsy values": "truthiness",
    "guarding invalid input (NaN, out of range)": "is_plausible_reading",
}

FALSY_EXAMPLES: tuple[object, ...] = (0, 0.0, "", [], {}, set(), None, False)


def compare(a: float, b: float) -> dict[str, bool]:
    """Every comparison operator applied to the same pair of numbers."""
    return {"==": a == b, "!=": a != b, "<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}


def is_plausible_reading(celsius: float) -> bool:
    """Reject NaN and physically implausible air temperatures.

    ``nan`` compares False with everything, so ``nan < 0`` and ``nan > 60`` are
    both False – without this guard it would silently slip through a ladder.
    """
    return not math.isnan(celsius) and -60 <= celsius <= 60


def classify_temperature(celsius: float) -> str:
    """Bucket a temperature using chained comparisons in an ``elif`` ladder."""
    if not is_plausible_reading(celsius):
        raise ValueError(f"implausible temperature: {celsius}")
    if celsius < 0:
        return "freezing"
    elif 0 <= celsius < 10:
        return "cold"
    elif 10 <= celsius < 20:
        return "mild"
    elif 20 <= celsius < 30:
        return "warm"
    else:
        return "hot"


def hike_decision(celsius: float, rain_mm: float, wind_kmh: float, has_guide: bool) -> tuple[bool, list[str]]:
    """Return (go?, packing list) using nested conditions."""
    band = classify_temperature(celsius)
    packing: list[str] = ["water"]
    if band in {"freezing", "cold"}:
        packing.append("insulated jacket")
        if band == "freezing":
            packing.append("crampons")
    elif band == "hot":
        packing.extend(["sun hat", "extra water"])

    if rain_mm > 0:
        packing.append("rain shell")

    if wind_kmh >= 60:
        go = False  # too dangerous for anyone
    elif wind_kmh >= 40 or rain_mm >= 20:
        go = has_guide  # risky: only with a guide
    else:
        go = band != "freezing" or has_guide
    return go, packing


def truthiness(value: object) -> str:
    """Describe how ``if value:`` would treat *value*."""
    return "truthy" if value else "falsy"


def summarize_notes(notes: str) -> str:
    """Truthy/falsy in practice: an empty string means 'no notes'."""
    return notes.strip() or "(no notes)"


def main() -> None:
    print("Day 08 – Hiking weather advisor\n")
    print("compare(3, 5):", compare(3, 5))
    for temp, rain, wind, guide in [(-5, 0, 10, False), (-5, 0, 10, True), (24, 25, 15, False),
                                    (33, 0, 65, True), (12, 2, 20, False)]:
        go, packing = hike_decision(temp, rain, wind, guide)
        verdict = "GO" if go else "STAY"
        print(f"{temp:>4}°C rain={rain:>2} wind={wind:>2} guide={guide!s:<5} → {verdict:<4} "
              f"pack: {', '.join(packing)}")
    print("\nFalsy values:", ", ".join(repr(v) for v in FALSY_EXAMPLES))
    print("Notes:", summarize_notes("   "))
    print("NaN accepted?", is_plausible_reading(float("nan")))


if __name__ == "__main__":
    main()
