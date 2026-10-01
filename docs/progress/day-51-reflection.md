# Day 51 – Try / Except / Raise Reflection

**Date:** 2026-05-02 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_51_try_except_raise/main.py`](../../src/day_51_try_except_raise/main.py) · **Tests:** [`tests/test_day_51.py`](../../tests/test_day_51.py) (11 tests)

## Scenario
A *concert ticket booking service* with its own exception hierarchy, so callers can catch errors as broadly or as precisely as they need.

## Syllabus deliverables
> Raising custom exceptions and exception hierarchy design

| Deliverable | Implemented in |
|---|---|
| ✅ custom exception base class | `BookingError` |
| ✅ exception hierarchy design | `exception_tree` |
| ✅ exceptions carrying data | `SeatUnavailableError` |
| ✅ raise | `BookingService.book` |
| ✅ catching by level of the hierarchy | `handle_booking` |
| ✅ translating low-level errors (raise from) | `BookingService.charge` |

## Key learnings
- One base exception per domain lets callers catch everything with a single `except`.
- Categories (validation, availability, payment) let callers react differently.
- Exceptions can carry data (`seats`, `requested`, `limit`) for precise messages.

## Pitfalls I hit (and how I fixed them)
- Catch the most specific classes first – a base-class `except` placed earlier would swallow them.

## Run it
```bash
./propython.sh 51                 # study mode: explanation, code map, notes and tests
python -m src.day_51_try_except_raise.main
pytest tests/test_day_51.py -v
```

## Next step
- Reuse the hierarchy pattern in the validation library (Day 94).
