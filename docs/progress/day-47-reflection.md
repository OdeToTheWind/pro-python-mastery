# Day 47 – Packing and Unpacking Functions in Python Reflection

**Date:** 2026-04-28 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_47_packing_unpacking/main.py`](../../src/day_47_packing_unpacking/main.py) · **Tests:** [`tests/test_day_47.py`](../../tests/test_day_47.py) (10 tests)

## Scenario
A *GPS route planner* – coordinates, waypoints and connection settings are passed around as tuples and dicts, then unpacked straight into function calls.

## Syllabus deliverables
> Advanced argument unpacking with \* and \*\*

| Deliverable | Implemented in |
|---|---|
| ✅ \* unpacking at the call site | `leg_distance` |
| ✅ \*\* unpacking at the call site | `connect` |
| ✅ packing with \*args | `route_length` |
| ✅ packing with \*\*kwargs | `connect` |
| ✅ extended unpacking (first, \*middle, last) | `split_route` |
| ✅ merging with [\*a, \*b] and {\*\*a, \*\*b} | `merge_settings` |
| ✅ unzipping with zip(\*pairs) | `unzip` |
| ✅ swap via tuple packing/unpacking | `swap_ends` |

## Key learnings
- `f(*seq)` spreads a sequence into positional arguments; `f(**mapping)` spreads keys into keyword arguments.
- `first, *middle, last = seq` unpacks any length of sequence.
- `zip(*pairs)` transposes a list of pairs.

## Pitfalls I hit (and how I fixed them)
- `**` unpacking still enforces the signature – a missing required key raises `TypeError`.

## Run it
```bash
python -m src.day_47_packing_unpacking.main
pytest tests/test_day_47.py -v
```

## Next step
- Use argument forwarding inside decorators (Day 67).
