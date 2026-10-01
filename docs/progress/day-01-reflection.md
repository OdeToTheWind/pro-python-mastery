# Day 01 – Variables, Type Hinting & Scoping Reflection

**Date:** 2026-03-13 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_01_variables/main.py`](../../src/day_01_variables/main.py) · **Tests:** [`tests/test_day_01.py`](../../tests/test_day_01.py) (10 tests)

## Scenario
A *learning-streak tracker* that records study sessions.

## Syllabus deliverables
> Strict typing with PEP 484/695, f-strings, scope rules, local vs global vs nonlocal

| Deliverable | Implemented in |
|---|---|
| ✅ PEP 484 annotations | `format_status` |
| ✅ PEP 695 type alias + generic function | `first_or_default` |
| ✅ f-strings with format specs | `format_status` |
| ✅ global scope (global keyword) | `record_session` |
| ✅ enclosing scope (nonlocal keyword) | `make_streak_counter` |
| ✅ local scope shadowing a global | `shadowing_demo` |

## Key learnings
- PEP 695 `type` aliases and `def f[T]` make generic intent readable without importing `TypeVar`.
- Reading a global needs no keyword; *rebinding* it needs `global`, and rebinding an enclosing variable needs `nonlocal`.
- Format specs (`:<12`, `:03d`, `:,`, `!r`) belong inside the f-string, not in manual padding code.

## Pitfalls I hit (and how I fixed them)
- Forgetting `global` turns `total += x` into an `UnboundLocalError` because assignment makes the name local for the whole function.
- Module-level state leaks between tests – an autouse fixture now resets it.

## Run it
```bash
python -m src.day_01_variables.main
pytest tests/test_day_01.py -v
```

## Next step
- Revisit scope on Day 23 with the full LEGB walk-through and closures' `__closure__` cells.
