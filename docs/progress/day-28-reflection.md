# Day 28 – Creating Classes in Python Reflection

**Date:** 2026-04-09 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_28_classes/main.py`](../../src/day_28_classes/main.py) · **Tests:** [`tests/test_day_28.py`](../../tests/test_day_28.py) (7 tests)

## Scenario
A *community library catalogue* – a ``Book`` class with an initialiser, instance attributes, behaviour methods and friendly dunders.

## Syllabus deliverables
> Defining classes, \_\_init\_\_, instance attributes and methods

| Deliverable | Implemented in |
|---|---|
| ✅ defining a class | `Book` |
| ✅ \_\_init\_\_ | `Book.__init__` |
| ✅ instance attributes | `Book.__init__` |
| ✅ class attributes | `Book.LOAN_DAYS` |
| ✅ methods | `Book.check_out` |
| ✅ dunder methods | `Book.__repr__` |

## Key learnings
- `__init__` should leave the object in a valid state or raise.
- Class attributes are shared; instance attributes belong to one object.
- `__eq__` and `__hash__` must agree when objects go into sets or dict keys.

## Pitfalls I hit (and how I fixed them)
- Updating a class counter through `self.counter += 1` would create an instance attribute – use the class name.

## Run it
```bash
python -m src.day_28_classes.main
pytest tests/test_day_28.py -v
```

## Next step
- Replace boilerplate with `@dataclass` where behaviour is simple (Day 32).
