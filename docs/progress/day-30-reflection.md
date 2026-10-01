# Day 30 – Getting / Setting Attributes Reflection

**Date:** 2026-04-11 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_30_getting_setting_attributes/main.py`](../../src/day_30_getting_setting_attributes/main.py) · **Tests:** [`tests/test_day_30.py`](../../tests/test_day_30.py) (8 tests)

## Scenario
A *smart thermostat* whose temperature can be read and written in Celsius or Fahrenheit, but never set to an unsafe value.

## Syllabus deliverables
> @property, getters, setters, and controlled attribute access

| Deliverable | Implemented in |
|---|---|
| ✅ @property getter | `Thermostat.celsius` |
| ✅ setter with validation | `Thermostat.celsius` |
| ✅ computed property with setter | `Thermostat.fahrenheit` |
| ✅ read-only property | `Thermostat.history` |
| ✅ deleter | `Thermostat.schedule` |
| ✅ dynamic getattr/setattr/hasattr | `apply_settings` |

## Key learnings
- Route `__init__` through the property setter so validation can't be bypassed.
- Computed properties (`fahrenheit`) avoid storing the same fact twice.
- `getattr`/`setattr` still trigger properties, so dynamic configuration stays validated.

## Pitfalls I hit (and how I fixed them)
- The original `Person` accepted a negative age because the constructor wrote `_age` directly.

## Run it
```bash
./propython.sh 30                 # study mode: explanation, code map, notes and tests
python -m src.day_30_getting_setting_attributes.main
pytest tests/test_day_30.py -v
```

## Next step
- See how `@property` is built from descriptors on Day 69.
