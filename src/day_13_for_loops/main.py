"""Day 13 – For Loops.

Scenario: a *school sports-day results board* – iterate over athletes,
lanes and heats to build tables and rankings.

Deliverables (syllabus):
* ``for`` loops and ``range()``
* ``enumerate()`` and ``zip()``
* Nested loops
* Tables and iteration (plus ``for ... else``)
"""

from __future__ import annotations

DELIVERABLES: dict[str, str] = {
    "for + range()": "lane_numbers",
    "enumerate()": "ranking_board",
    "zip()": "pair_results",
    "nested loops": "heat_table",
    "tables": "multiplication_table",
    "for ... else": "first_disqualified",
}


def lane_numbers(start: int, stop: int, step: int = 1) -> list[int]:
    """Lanes via ``range(start, stop, step)``; ``stop`` is exclusive and step may be negative."""
    if step == 0:
        raise ValueError("step cannot be zero – range() would never finish")
    return [lane for lane in range(start, stop, step)]


def pair_results(names: list[str], times: list[float]) -> list[tuple[str, float]]:
    """Combine two parallel lists. ``strict=True`` catches length mismatches."""
    return list(zip(names, times, strict=True))


def ranking_board(results: list[tuple[str, float]]) -> list[str]:
    """Rank by time using ``enumerate(start=1)``; ties share a place."""
    lines: list[str] = []
    previous_time: float | None = None
    place = 0
    for position, (name, seconds) in enumerate(sorted(results, key=lambda r: r[1]), start=1):
        if seconds != previous_time:
            place = position
        previous_time = seconds
        lines.append(f"{place:>2}. {name:<10} {seconds:>6.2f}s")
    return lines


def heat_table(heats: int, lanes: int) -> list[list[str]]:
    """Nested loops: one row per heat, one cell per lane (e.g. ``H2-L3``)."""
    table: list[list[str]] = []
    for heat in range(1, heats + 1):
        row = []
        for lane in range(1, lanes + 1):
            row.append(f"H{heat}-L{lane}")
        table.append(row)
    return table


def multiplication_table(size: int) -> str:
    """Classic grid built with two nested loops and right-aligned columns."""
    width = len(str(size * size)) + 1
    rows = []
    for i in range(1, size + 1):
        rows.append("".join(f"{i * j:>{width}}" for j in range(1, size + 1)))
    return "\n".join(rows)


def first_disqualified(results: list[tuple[str, float]], limit: float) -> str:
    """``for ... else``: the ``else`` runs only when the loop did **not** ``break``."""
    for name, seconds in results:
        if seconds > limit:
            message = f"{name} exceeded the {limit}s limit"
            break
    else:
        message = "everyone finished within the limit"
    return message


def main() -> None:
    names = ["Asha", "Ben", "Chen", "Dara"]
    times = [12.4, 11.9, 12.4, 13.8]
    print("Day 13 – Sports-day results\n")
    print("Lanes:", lane_numbers(1, 9), "| reverse:", lane_numbers(8, 0, -2))
    results = pair_results(names, times)
    print("\n".join(ranking_board(results)))
    print("\nHeat grid:")
    for row in heat_table(2, 4):
        print("  " + " ".join(row))
    print("\n" + multiplication_table(5))
    print("\n" + first_disqualified(results, 13.0))


if __name__ == "__main__":
    main()
