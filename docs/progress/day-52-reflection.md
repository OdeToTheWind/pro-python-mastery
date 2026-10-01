# Day 52 – Working with JSONs Reflection

**Date:** 2026-05-03 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_52_working_with_jsons/main.py`](../../src/day_52_working_with_jsons/main.py) · **Tests:** [`tests/test_day_52.py`](../../tests/test_day_52.py) (11 tests)

## Scenario
A *weather-station API client* that receives JSON payloads, validates them into typed objects, and serialises its own reports – including types JSON doesn't support natively (datetime, Decimal, dataclasses).

## Syllabus deliverables
> JSON serialization, parsing and payload handling

| Deliverable | Implemented in |
|---|---|
| ✅ serialisation with a custom encoder | `to_json` |
| ✅ pretty vs compact output | `to_json` |
| ✅ parsing with object\_hook / parse\_float | `from_json` |
| ✅ payload validation | `parse_reading` |
| ✅ file save/load with corruption handling | `load_json` |

## Key learnings
- A custom `JSONEncoder` handles datetime, Decimal, dataclasses and sets explicitly.
- `parse_float=Decimal` keeps money exact; `object_hook` revives timestamps.
- Validate payloads into typed objects at the boundary, then trust them inside.

## Pitfalls I hit (and how I fixed them)
- `default=str` silently turned unknown objects into strings – unknown types must raise.

## Run it
```bash
python -m src.day_52_working_with_jsons.main
pytest tests/test_day_52.py -v
```

## Next step
- Validate with dataclasses/pydantic in the config system (Day 91).
