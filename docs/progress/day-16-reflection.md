# Day 16 – Flowchart Programming Reflection

**Date:** 2026-03-28 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_16_flowchart_programming/main.py`](../../src/day_16_flowchart_programming/main.py) · **Tests:** [`tests/test_day_16.py`](../../tests/test_day_16.py) (7 tests)

## Scenario
A *public library desk* – loan approvals, overdue fines and a returns-sorting conveyor, each first drawn as a flowchart and then translated into Python.

## Syllabus deliverables
> Translating logic flowcharts into if-elif-else and loop structures

| Deliverable | Implemented in |
|---|---|
| ✅ decision diamonds → if/elif/else | `loan_decision` |
| ✅ process boxes and thresholds | `overdue_fine` |
| ✅ loop arrows → while | `sort_returns` |
| ✅ flowchart as data | `run_flowchart` |

## Key learnings
- Each decision diamond maps to one condition in the same order as the drawing.
- Loop arrows become `while queue:`; process boxes become plain statements.
- Storing a flowchart as data lets one interpreter run many charts, and it can detect cycles.

## Pitfalls I hit (and how I fixed them)
- A flowchart test is strongest when it checks that the coded version and the data version agree for every input combination.

## Run it
```bash
python -m src.day_16_flowchart_programming.main
pytest tests/test_day_16.py -v
```

## Next step
- Grow the data-driven idea into the plugin registry on Day 87.
