"""Day 16 – Flowchart Programming.

Scenario: a *public library desk* – loan approvals, overdue fines and a
returns-sorting conveyor, each first drawn as a flowchart and then translated
into Python.

Deliverables (syllabus):
* Translating logic flowcharts into ``if / elif / else``
* Translating flowchart loops into ``while`` / ``for`` structures
* (bonus) a tiny data-driven flowchart interpreter
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

DELIVERABLES: dict[str, str] = {
    "decision diamonds → if/elif/else": "loan_decision",
    "process boxes and thresholds": "overdue_fine",
    "loop arrows → while": "sort_returns",
    "flowchart as data": "run_flowchart",
}

LOAN_FLOWCHART = """
(START) → <member active?> -no→ [REFUSE: renew membership]
              │yes
              ▼
          <fines > €5?> -yes→ [REFUSE: pay fines]
              │no
              ▼
          <books out < limit?> -no→ [REFUSE: limit reached]
              │yes
              ▼
          [APPROVE] → (END)
"""


def loan_decision(*, active: bool, fines: float, books_out: int, limit: int = 5) -> str:
    """Each diamond in ``LOAN_FLOWCHART`` becomes one condition, in the same order."""
    if not active:
        return "refuse: renew membership"
    elif fines > 5:
        return "refuse: pay fines"
    elif books_out >= limit:
        return "refuse: limit reached"
    else:
        return "approve"


def overdue_fine(days_late: int, *, is_child: bool = False) -> float:
    """Tiered fine flowchart: free grace day, €0.25/day up to a week, then €0.50/day, capped."""
    if days_late < 0:
        raise ValueError("days_late cannot be negative")
    if days_late <= 1:
        fine = 0.0
    elif days_late <= 7:
        fine = 0.25 * (days_late - 1)
    else:
        fine = 0.25 * 6 + 0.50 * (days_late - 7)
    fine = min(fine, 10.0)
    return round(fine / 2 if is_child else fine, 2)


def sort_returns(conveyor: list[str]) -> dict[str, list[str]]:
    """Loop arrow ``while items remain`` → decision 'which shelf?' → back to the loop."""
    shelves: dict[str, list[str]] = {"fiction": [], "science": [], "repair": []}
    queue = list(conveyor)
    while queue:
        item = queue.pop(0)
        if item.endswith("!"):
            shelves["repair"].append(item.rstrip("!"))
        elif item.startswith("SCI-"):
            shelves["science"].append(item)
        else:
            shelves["fiction"].append(item)
    return shelves


@dataclass(frozen=True, slots=True)
class Decision:
    question: str
    yes: str
    no: str


Flowchart = Mapping[str, Decision | str]


def run_flowchart(chart: Flowchart, answers: Mapping[str, bool], start: str = "start") -> list[str]:
    """Walk a flowchart stored as data. Strings are terminal boxes; returns the path taken."""
    path = [start]
    node = chart[start]
    steps = 0
    while isinstance(node, Decision):
        steps += 1
        if steps > len(chart):
            raise RuntimeError("flowchart contains a cycle")
        next_key = node.yes if answers[node.question] else node.no
        path.append(next_key)
        node = chart[next_key]
    path.append(node)
    return path


LOAN_CHART: dict[str, Decision | str] = {
    "start": Decision("active", yes="fines", no="renew"),
    "fines": Decision("owes_over_5", yes="pay", no="limit"),
    "limit": Decision("under_limit", yes="approve", no="full"),
    "renew": "REFUSE: renew membership",
    "pay": "REFUSE: pay fines",
    "full": "REFUSE: limit reached",
    "approve": "APPROVE",
}


def main() -> None:
    print("Day 16 – Library desk flowcharts")
    print(LOAN_FLOWCHART)
    print("Coded:", loan_decision(active=True, fines=2, books_out=1))
    print("Data :", " → ".join(run_flowchart(
        LOAN_CHART, {"active": True, "owes_over_5": False, "under_limit": True})))
    for days in (0, 3, 10, 40):
        print(f"fine for {days:>2} day(s) late: €{overdue_fine(days):.2f}")
    print(sort_returns(["Dune", "SCI-Cosmos", "Emma!", "SCI-Genes!"]))


if __name__ == "__main__":
    main()
