# Day 07 – Converting Types (Casting) Reflection

**Date:** 2026-03-19 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_07_converting_types/main.py`](../../src/day_07_converting_types/main.py) · **Tests:** [`tests/test_day_07.py`](../../tests/test_day_07.py) (6 tests)

## Scenario
A *spreadsheet import cleaner* – every cell arrives as text and must be cast to the right Python type, with precise error reporting.

## Syllabus deliverables
> int(), float(), str(), bool(), list(), tuple(), set(), dict(), ValueError vs TypeError

| Deliverable | Implemented in |
|---|---|
| ✅ int/float/str/bool casts | `convert` |
| ✅ list/tuple/set/dict casts | `convert` |
| ✅ parsing collections from text | `parse_collection` |
| ✅ bool('False') pitfall and strict parsing | `parse_bool` |
| ✅ ValueError vs TypeError | `error_examples` |

## Key learnings
- `ValueError` means the type is right but the content is wrong (`int('abc')`); `TypeError` means the type itself is wrong (`int(None)`).
- `bool('False')` is `True` – parse yes/no words explicitly.
- `ast.literal_eval` safely turns text such as `"[1, 2]"` into Python objects.

## Pitfalls I hit (and how I fixed them)
- `int(float('inf'))` raises `OverflowError`, a third error class the converter must catch.

## Run it
```bash
python -m src.day_07_converting_types.main
pytest tests/test_day_07.py -v
```

## Next step
- Use these converters to clean CSV fields on Day 43.
