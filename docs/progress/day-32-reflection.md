# Day 32 – Class Initialisers Reflection

**Date:** 2026-04-13 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_32_class_initialisers/main.py`](../../src/day_32_class_initialisers/main.py) · **Tests:** [`tests/test_day_32.py`](../../tests/test_day_32.py) (9 tests)

## Scenario
*opening bank accounts* – the constructor is the gatekeeper that guarantees every account object is valid from the first moment it exists.

## Syllabus deliverables
> \_\_init\_\_ constructors, defaults, validation and object setup

| Deliverable | Implemented in |
|---|---|
| ✅ \_\_init\_\_ constructor | `BankAccount.__init__` |
| ✅ defaults | `BankAccount.__init__` |
| ✅ validation in the constructor | `BankAccount.__init__` |
| ✅ object setup (ids, derived state) | `BankAccount.__init__` |
| ✅ mutable default trap | `BadAccount` |
| ✅ dataclass \_\_post\_init\_\_ | `SavingsGoal` |

## Key learnings
- Reject invalid state in `__init__` rather than silently 'fixing' it.
- A mutable default is created once at definition time; use `None` or `default_factory`.
- `__post_init__` adds validation and derived fields to dataclasses.

## Pitfalls I hit (and how I fixed them)
- `print()` inside a constructor is a side effect that makes objects noisy to create in tests.

## Run it
```bash
python -m src.day_32_class_initialisers.main
pytest tests/test_day_32.py -v
```

## Next step
- Use validated dataclasses in the type-safe config system (Day 91).
