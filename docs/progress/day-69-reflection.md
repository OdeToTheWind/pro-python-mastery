# Day 69 – Descriptors Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_69_descriptors/main.py`](../../src/day_69_descriptors/main.py) · **Tests:** [`tests/test_day_69.py`](../../tests/test_day_69.py) (11 tests)

## Scenario
A *hotel-booking form model* whose fields validate themselves – the same machinery behind Django/SQLAlchemy model fields, ``@property``, ``@classmethod`` and bound methods.

## Syllabus deliverables
> Data and non-data descriptors; how @property works under the hood

| Deliverable | Implemented in |
|---|---|
| ✅ data descriptor with \_\_set\_name\_\_ | `Field` |
| ✅ validated descriptor subclasses | `PositiveInt` |
| ✅ non-data descriptor (cached value) | `cached` |
| ✅ lookup precedence: data > instance dict > non-data | `precedence_demo` |
| ✅ @property re-implemented | `MyProperty` |
| ✅ functions are non-data descriptors (bound methods) | `bound_method_demo` |

## Key learnings
- A descriptor is any class attribute with `__get__`; adding `__set__`/`__delete__` makes it a data descriptor.
- Lookup order: data descriptors → instance `__dict__` → non-data descriptors → class attributes.
- `__set_name__` tells a descriptor which attribute name it was assigned to, so one class serves many fields.

## Pitfalls I hit (and how I fixed them)
- A cached non-data descriptor is shadowed by the instance dict after the first access – that is the trick, not a bug.

## Run it
```bash
./propython.sh 69                 # study mode: explanation, code map, notes and tests
python -m src.day_69_descriptors.main
pytest tests/test_day_69.py -v
```

## Next step
- Look one level deeper at what creates classes themselves on Day 70.
