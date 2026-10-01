# Day 11 – Error Handling Reflection

**Date:** 2026-03-23 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_11_error_handling/main.py`](../../src/day_11_error_handling/main.py) · **Tests:** [`tests/test_day_11.py`](../../tests/test_day_11.py) (10 tests)

## Scenario
A *greenhouse sensor log reader* – log files are messy, devices disappear and humans type bad values. The program must keep going.

## Syllabus deliverables
> try/except/else/finally, common exceptions and robust user input handling

| Deliverable | Implemented in |
|---|---|
| ✅ try/except/else/finally | `load_readings` |
| ✅ common exceptions | `provoke` |
| ✅ robust user input | `ask_float` |
| ✅ graceful recovery from bad data | `parse_line` |

## Key learnings
- `else` runs only when the `try` succeeded; `finally` always runs – ideal for closing resources.
- Catch the narrowest exception that you can actually handle.
- Bad lines in a data file should be reported and skipped, not crash the whole import.

## Pitfalls I hit (and how I fixed them)
- A `KeyError` message already contains quotes, so wrapping it in more quotes printed `''zzz''`.

## Run it
```bash
python -m src.day_11_error_handling.main
pytest tests/test_day_11.py -v
```

## Next step
- Build an exception hierarchy of my own on Day 51.
