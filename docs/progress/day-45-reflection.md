# Day 45 – List Comprehensions Reflection

**Date:** 2026-04-26 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_45_list_comprehensions/main.py`](../../src/day_45_list_comprehensions/main.py) · **Tests:** [`tests/test_day_45.py`](../../tests/test_day_45.py) (10 tests)

## Scenario
A *web-server log analyser* – raw access-log lines become clean, filtered, transformed lists in one readable expression each.

## Syllabus deliverables
> Concise creation, filtering and transformation of sequences

| Deliverable | Implemented in |
|---|---|
| ✅ creation | `status_codes` |
| ✅ filtering | `server_errors` |
| ✅ transformation | `normalise_paths` |
| ✅ conditional expression inside | `status_labels` |
| ✅ nested comprehension (flatten / matrix) | `transpose` |
| ✅ walrus operator in a comprehension | `slow_requests` |
| ✅ comprehension vs loop vs generator | `loop_equivalent` |

## Key learnings
- A comprehension has three parts: output expression, `for` clause(s), optional `if` filter.
- A conditional *expression* in the output is different from a filter.
- The walrus operator avoids computing the same value twice.

## Pitfalls I hit (and how I fixed them)
- Large intermediate lists waste memory; a generator expression is tiny by comparison.

## Run it
```bash
python -m src.day_45_list_comprehensions.main
pytest tests/test_day_45.py -v
```

## Next step
- Move to full generators and pipelines on Days 65–66.
