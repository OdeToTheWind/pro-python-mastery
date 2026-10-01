# Day 55 – Working with Date and Time Reflection

**Date:** 2026-05-06 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_55_date_and_time/main.py`](../../src/day_55_date_and_time/main.py) · **Tests:** [`tests/test_day_55.py`](../../tests/test_day_55.py) (10 tests)

## Scenario
A *global team meeting planner* – ages, deadlines, business days and one meeting shown in every teammate's local time.

## Syllabus deliverables
> datetime usage, calculations, formatting and timezone awareness

| Deliverable | Implemented in |
|---|---|
| ✅ exact age calculation | `age_on` |
| ✅ business-day arithmetic | `add_business_days` |
| ✅ parsing several formats | `parse_date` |
| ✅ formatting | `humanize_delta` |
| ✅ timezone-aware conversion | `meeting_in_zones` |
| ✅ DST awareness | `utc_offset_hours` |
| ✅ aware 'now' in UTC | `now_utc` |

## Key learnings
- Store and compare times in UTC; convert with `zoneinfo` only for display.
- Exact age compares (month, day) tuples – `days // 365` is wrong near birthdays.
- The same wall-clock time has different UTC offsets in winter and summer (DST).

## Pitfalls I hit (and how I fixed them)
- `datetime.now()` without a timezone is naive and can't be compared with aware times.

## Run it
```bash
python -m src.day_55_date_and_time.main
pytest tests/test_day_55.py -v
```

## Next step
- Schedule recurring jobs across time zones on Day 89.
