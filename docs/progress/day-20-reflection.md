# Day 20 – Returning Functions Reflection

**Date:** 2026-04-01 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_20_returning_functions/main.py`](../../src/day_20_returning_functions/main.py) · **Tests:** [`tests/test_day_20.py`](../../tests/test_day_20.py) (10 tests)

## Scenario
A *blog post analyser* – functions that return values, multiple values, exit early on bad input, return other functions and compose into a text-processing pipeline.

## Syllabus deliverables
> return statements, returning multiple values, early returns and function composition

| Deliverable | Implemented in |
|---|---|
| ✅ return statement | `reading_time` |
| ✅ returning multiple values (tuple unpacking) | `text_stats` |
| ✅ early returns / guard clauses | `validate_title` |
| ✅ functions that return functions | `make_truncator` |
| ✅ function composition | `compose` |

## Key learnings
- Returning a tuple and unpacking it is Python's way to return multiple values.
- Guard clauses keep functions flat: handle the bad cases first, then the main path.
- Functions are values – `make_truncator` returns one and `compose` chains many.

## Pitfalls I hit (and how I fixed them)
- Returning `(0, 0, 0, 0)` for empty input was ambiguous; empty input is now handled explicitly.

## Run it
```bash
./propython.sh 20                 # study mode: explanation, code map, notes and tests
python -m src.day_20_returning_functions.main
pytest tests/test_day_20.py -v
```

## Next step
- Write decorators – functions that take and return functions – on Day 67.
