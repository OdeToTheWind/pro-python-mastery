# Day 18 – Python Dictionaries and Lists Reflection

**Date:** 2026-03-30 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_18_dictionaries_lists/main.py`](../../src/day_18_dictionaries_lists/main.py) · **Tests:** [`tests/test_day_18.py`](../../tests/test_day_18.py) (11 tests)

## Scenario
A *neighbourhood grocery store* – a dict-based inventory behind the counter and a list-based shopping cart in front of it.

## Syllabus deliverables
> List and dict methods, inventory management, shopping cart logic

| Deliverable | Implemented in |
|---|---|
| ✅ list methods | `list_method_tour` |
| ✅ dict methods | `Inventory` |
| ✅ inventory management | `Inventory` |
| ✅ shopping cart logic | `Cart` |

## Key learnings
- `dict.get(key, default)` and `setdefault` avoid `KeyError` boilerplate.
- A checkout should be all-or-nothing: validate every line first, then mutate.
- List methods mutate in place and return `None` (`sort`, `append`, `remove`).

## Pitfalls I hit (and how I fixed them)
- The previous day's file re-used Day 17 functions, so the real inventory logic was untested.

## Run it
```bash
./propython.sh 18                 # study mode: explanation, code map, notes and tests
python -m src.day_18_dictionaries_lists.main
pytest tests/test_day_18.py -v
```

## Next step
- Persist the inventory to JSON on Day 52.
