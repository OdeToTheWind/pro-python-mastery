# Day 17 – Positional and Keyword Arguments Reflection

**Date:** 2026-03-29 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_17_positional_keyword_arguments/main.py`](../../src/day_17_positional_keyword_arguments/main.py) · **Tests:** [`tests/test_day_17.py`](../../tests/test_day_17.py) (12 tests)

## Scenario
An *airline booking API* where some arguments must be positional (route), some must be named (cabin, flexibility) and some are optional.

## Syllabus deliverables
> Positional vs keyword arguments, defaults and argument flexibility

| Deliverable | Implemented in |
|---|---|
| ✅ positional arguments | `book_flight` |
| ✅ keyword arguments | `book_flight` |
| ✅ positional-only parameters (/) | `book_flight` |
| ✅ keyword-only parameters (\*) | `book_flight` |
| ✅ default values | `book_flight` |
| ✅ argument flexibility (\*names, \*\*titles) | `boarding_announcement` |
| ✅ inspecting how arguments bind | `how_arguments_bind` |

## Key learnings
- `/` makes parameters positional-only so they can be renamed later; `*` makes the rest keyword-only so they can't be mixed up.
- A default placed *before* `*args` can never be used together with extra positionals.
- `inspect.signature(...).bind()` shows exactly how a call maps onto parameters.

## Pitfalls I hit (and how I fixed them)
- The old `flexible_greeting('Alice', 'Bob')` treated Alice as the greeting and printed double spaces.

## Run it
```bash
./propython.sh 17                 # study mode: explanation, code map, notes and tests
python -m src.day_17_positional_keyword_arguments.main
pytest tests/test_day_17.py -v
```

## Next step
- Use keyword-only flags for every boolean option from now on.
