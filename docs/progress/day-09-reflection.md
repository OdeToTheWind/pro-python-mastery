# Day 09 – Logical Operations Reflection

**Date:** 2026-03-21 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_09_logical_operations/main.py`](../../src/day_09_logical_operations/main.py) · **Tests:** [`tests/test_day_09.py`](../../tests/test_day_09.py) (9 tests)

## Scenario
An *office building access controller* deciding who may open which door, and a tracer that proves when Python stops evaluating.

## Syllabus deliverables
> and, or, not, short-circuit evaluation, combining comparisons and access control

| Deliverable | Implemented in |
|---|---|
| ✅ and / or / not truth table | `truth_table` |
| ✅ short-circuit evaluation | `ShortCircuitTracer` |
| ✅ or/and return operands (not just bools) | `display_name` |
| ✅ combining comparisons | `within_hours` |
| ✅ access control | `can_open` |

## Key learnings
- `and`/`or` return one of their *operands*, not necessarily `True`/`False`.
- Short-circuiting is observable: a tracer shows the right operand never runs.
- Name sub-conditions (`is_staff`) before combining them so access rules stay readable.

## Pitfalls I hit (and how I fixed them)
- Using `print()` as an operand always yields `None`, so the original demo printed the wrong branch.

## Run it
```bash
python -m src.day_09_logical_operations.main
pytest tests/test_day_09.py -v
```

## Next step
- Model the door rules as data (a permission table) when building plugins on Day 87.
