# Day 02 – String Manipulation Reflection

**Date:** 2026-03-14 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_02_strings/main.py`](../../src/day_02_strings/main.py) · **Tests:** [`tests/test_day_02.py`](../../tests/test_day_02.py) (8 tests)

## Scenario
A *conference badge printer* that turns messy sign-up data into clean, aligned badges.

## Syllabus deliverables
> Advanced string methods, cleaning input, string formatting and alignment

| Deliverable | Implemented in |
|---|---|
| ✅ advanced string methods | `make_handle` |
| ✅ cleaning input | `clean_name` |
| ✅ slug / normalisation | `slugify` |
| ✅ formatting and alignment | `render_badge` |
| ✅ tabular alignment | `align_columns` |

## Key learnings
- `str.title()` capitalises after apostrophes (`John'S`); `string.capwords` plus a hyphen rule handles real names.
- `casefold()` is the right tool for case-insensitive work, not `lower()`.
- Alignment (`^`, `<`, `>`) and fill characters (`:.^32`) produce fixed-width output with no manual maths.

## Pitfalls I hit (and how I fixed them)
- Building a handle from a name with no letters produced `@05` – now it is rejected with `ValueError`.

## Run it
```bash
python -m src.day_02_strings.main
pytest tests/test_day_02.py -v
```

## Next step
- Use the slug and alignment helpers again when formatting reports on Day 21.
