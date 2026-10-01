# Day 06 – Built-in Data Types Reflection

**Date:** 2026-03-18 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_06_data_types/main.py`](../../src/day_06_data_types/main.py) · **Tests:** [`tests/test_day_06.py`](../../tests/test_day_06.py) (8 tests)

## Scenario
A *value inspector* – paste any Python literal and get a report on its type, category, mutability, hashability and size.

## Syllabus deliverables
> int, float, bool, str, list, tuple, dict, set, mutability and type checks

| Deliverable | Implemented in |
|---|---|
| ✅ core built-in types | `describe` |
| ✅ mutability | `describe` |
| ✅ aliasing consequences of mutability | `aliasing_demo` |
| ✅ type() vs isinstance() | `type_check_demo` |
| ✅ safe parsing of literals | `parse_literal` |

## Key learnings
- `bool` is a subclass of `int`, so `type(x) is int` and `isinstance(x, int)` disagree for `True`.
- Hashability is about the *contents*: `([1],)` is a tuple but `hash()` fails.
- Assignment never copies – two names can mutate the same list.

## Pitfalls I hit (and how I fixed them)
- Typing `None` in the explorer quit the program because `None` was also the quit signal.
- `sorted({1, 'a'})` raises `TypeError` – mixed sets need a key function.

## Run it
```bash
./propython.sh 6                 # study mode: explanation, code map, notes and tests
python -m src.day_06_data_types.main
pytest tests/test_day_06.py -v
```

## Next step
- Apply the hashability rule when choosing dict keys on Day 46.
