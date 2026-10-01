# Day 31 – Python Methods Reflection

**Date:** 2026-04-12 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_31_python_methods/main.py`](../../src/day_31_python_methods/main.py) · **Tests:** [`tests/test_day_31.py`](../../tests/test_day_31.py) (8 tests)

## Scenario
A *pizzeria ordering system* where each kind of method has a clear job: instance methods change one pizza, class methods build pizzas or change shop-wide settings, static methods are utilities that need neither.

## Syllabus deliverables
> Instance methods, class methods and static methods

| Deliverable | Implemented in |
|---|---|
| ✅ instance methods | `Pizza.add_topping` |
| ✅ class methods: alternative constructors | `Pizza.margherita` |
| ✅ class methods: shared class state | `Pizza.set_base_price` |
| ✅ static methods | `Pizza.valid_size` |

## Key learnings
- Instance methods change one object, class methods work with the class (alternative constructors), static methods are plain utilities.
- `cls(...)` in a classmethod returns the right subclass automatically.
- Class-level state changes should be scoped and restored (a context manager helps).

## Pitfalls I hit (and how I fixed them)
- A negative withdrawal used to *add* money – the new domain validates inputs inside the methods.

## Run it
```bash
./propython.sh 31                 # study mode: explanation, code map, notes and tests
python -m src.day_31_python_methods.main
pytest tests/test_day_31.py -v
```

## Next step
- Use classmethod constructors for config objects on Day 91.
