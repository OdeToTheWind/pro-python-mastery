# Day 46 – Dictionary Comprehensions Reflection

**Date:** 2026-04-27 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_46_dictionary_comprehensions/main.py`](../../src/day_46_dictionary_comprehensions/main.py) · **Tests:** [`tests/test_day_46.py`](../../tests/test_day_46.py) (9 tests)

## Scenario
An *online bookshop catalogue* – index products, reprice them, invert lookups and count words in reviews, each with a dict comprehension.

## Syllabus deliverables
> Efficient dictionary creation and transformation

| Deliverable | Implemented in |
|---|---|
| ✅ creation from a list of records | `index_by` |
| ✅ creation from two sequences (zip) | `price_list` |
| ✅ transformation of values | `apply_discount` |
| ✅ filtering by value | `filter_items` |
| ✅ inverting a mapping safely | `invert` |
| ✅ nested dict comprehension | `stock_matrix` |
| ✅ counting with a comprehension | `word_frequencies` |

## Key learnings
- Index records by key with `{r[key]: r for r in records}` for O(1) lookups.
- Inverting a mapping must handle duplicate values (map to lists).
- Set comprehensions (`{...}` without `:`) deduplicate inline.

## Pitfalls I hit (and how I fixed them)
- `apply_discount` must return a new dict; mutating the caller's prices was a hidden side effect.

## Run it
```bash
python -m src.day_46_dictionary_comprehensions.main
pytest tests/test_day_46.py -v
```

## Next step
- Combine with `Counter` and `defaultdict` on Day 71.
