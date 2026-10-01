# Day 13 – For Loops Reflection

**Date:** 2026-03-25 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_13_for_loops/main.py`](../../src/day_13_for_loops/main.py) · **Tests:** [`tests/test_day_13.py`](../../tests/test_day_13.py) (8 tests)

## Scenario
A *school sports-day results board* – iterate over athletes, lanes and heats to build tables and rankings.

## Syllabus deliverables
> for loops, range(), enumerate(), zip(), nested loops, tables and iteration

| Deliverable | Implemented in |
|---|---|
| ✅ for + range() | `lane_numbers` |
| ✅ enumerate() | `ranking_board` |
| ✅ zip() | `pair_results` |
| ✅ nested loops | `heat_table` |
| ✅ tables | `multiplication_table` |
| ✅ for ... else | `first_disqualified` |

## Key learnings
- `enumerate(start=1)` and `zip(strict=True)` remove manual index bookkeeping and catch length mismatches.
- `range(stop)` excludes `stop`; a zero step raises `ValueError`.
- `for ... else` runs the `else` only when no `break` happened – a clean 'not found' branch.

## Pitfalls I hit (and how I fixed them)
- Printing `start..end-1` was wrong for any step other than 1, so the label was removed.

## Run it
```bash
python -m src.day_13_for_loops.main
pytest tests/test_day_13.py -v
```

## Next step
- Replace loops with comprehensions where it improves clarity (Day 45).
