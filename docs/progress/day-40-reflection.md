# Day 40 – Python Slice Function Reflection

**Date:** 2026-04-21 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_40_python_slice_function/main.py`](../../src/day_40_python_slice_function/main.py) · **Tests:** [`tests/test_day_40.py`](../../tests/test_day_40.py) (12 tests)

## Scenario
A *bank-statement parser* for fixed-width text records, plus a playlist editor – both lean on slicing.

## Syllabus deliverables
> Advanced slicing techniques for lists and strings

| Deliverable | Implemented in |
|---|---|
| ✅ slice() objects as named fields | `parse_record` |
| ✅ slice.indices() | `describe_slice` |
| ✅ string slicing: steps and reversal | `mask_account` |
| ✅ list slicing: assignment | `replace_section` |
| ✅ list slicing: deletion | `drop_every_other` |
| ✅ rotation and chunking | `rotate` |
| ✅ guarding against step=0 | `safe_slice` |

## Key learnings
- Named `slice` objects make fixed-width parsing self-documenting.
- Slice assignment can grow or shrink a list in place; `del lst[::2]` deletes by pattern.
- `slice.indices(len)` reveals how `None`/negative bounds resolve.

## Pitfalls I hit (and how I fixed them)
- A zero step raises `ValueError` – validate before slicing user input.

## Run it
```bash
python -m src.day_40_python_slice_function.main
pytest tests/test_day_40.py -v
```

## Next step
- Use chunking for the large-file processor on Day 90.
