# Day 39 – Python Inheritance Reflection

**Date:** 2026-04-20 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_39_python_inheritance/main.py`](../../src/day_39_python_inheritance/main.py) · **Tests:** [`tests/test_day_39.py`](../../tests/test_day_39.py) (8 tests)

## Scenario
A *smart-device product line*. A base ``Device`` is specialised by single inheritance (``Camera``) and combined with capability mixins through multiple inheritance (``SmartDoorbell``) using cooperative ``super()``.

## Syllabus deliverables
> Single and multiple inheritance, super(), and method overriding

| Deliverable | Implemented in |
|---|---|
| ✅ single inheritance | `Camera` |
| ✅ multiple inheritance | `SmartDoorbell` |
| ✅ super() and cooperative \_\_init\_\_ | `WiFiMixin.__init__` |
| ✅ method overriding | `Camera.status` |
| ✅ method resolution order (MRO) | `mro_names` |
| ✅ isinstance / issubclass checks | `capabilities` |

## Key learnings
- Cooperative `super()` with `**kwargs` lets every class in the MRO initialise exactly once.
- Mixins add capabilities; put them before the concrete base class.
- Overrides can extend the parent result by calling `super().method()`.

## Pitfalls I hit (and how I fixed them)
- Forgetting `super().__init__(**kwargs)` in one class silently breaks the chain for everything after it.

## Run it
```bash
python -m src.day_39_python_inheritance.main
pytest tests/test_day_39.py -v
```

## Next step
- Compare inheritance with composition and protocols on Day 72.
