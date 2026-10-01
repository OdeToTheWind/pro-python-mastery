# Day 67 – Decorators Deep Dive Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_67_decorators_deep_dive/main.py`](../../src/day_67_decorators_deep_dive/main.py) · **Tests:** [`tests/test_day_67.py`](../../tests/test_day_67.py) (11 tests)

## Scenario
A *weather-service client toolkit* – cross-cutting concerns (timing, retries, caching per city, rate limiting, input validation) are added to plain functions with decorators instead of being copy-pasted.

## Syllabus deliverables
> Function decorators, @wraps, parameterized decorators, and class-based decorators

| Deliverable | Implemented in |
|---|---|
| ✅ function decorator | `timed` |
| ✅ @wraps preserves metadata | `timed` |
| ✅ decorator without wraps (the problem) | `naive_timed` |
| ✅ parameterised decorator | `retry` |
| ✅ decorator usable with and without arguments | `validate_range` |
| ✅ class-based decorator with state | `RateLimit` |
| ✅ decorator for caching | `memoize_by` |
| ✅ stacking order | `STACKING_ORDER` |

## Key learnings
- A decorator is a function that takes a function and returns a replacement; `@` is just assignment sugar.
- `functools.wraps` keeps `__name__`, `__doc__`, `__wrapped__` and the signature – without it tools and tests see `wrapper`.
- Parameterised decorators are factories (three levels); class-based decorators keep state on the instance.

## Pitfalls I hit (and how I fixed them)
- Stacked decorators are applied bottom-up but their wrappers run top-down – order matters for caching vs timing.

## Run it
```bash
./propython.sh 67                 # study mode: explanation, code map, notes and tests
python -m src.day_67_decorators_deep_dive.main
pytest tests/test_day_67.py -v
```

## Next step
- Use context managers for setup/teardown that decorators can't express cleanly (Day 68).
