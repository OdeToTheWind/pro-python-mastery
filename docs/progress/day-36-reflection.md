# Day 36 – Python Instances and State Reflection

**Date:** 2026-04-17 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_36_python_instances_and_state/main.py`](../../src/day_36_python_instances_and_state/main.py) · **Tests:** [`tests/test_day_36.py`](../../tests/test_day_36.py) (9 tests)

## Scenario
*food-delivery orders*. Every order object tracks its own state as it moves through a lifecycle (placed → cooking → out for delivery → delivered, or cancelled), records history, and releases resources when it closes.

## Syllabus deliverables
> Instance variables, state tracking and object lifecycle patterns

| Deliverable | Implemented in |
|---|---|
| ✅ instance variables | `Order.__init__` |
| ✅ class variables | `Order.open_orders` |
| ✅ state tracking with allowed transitions | `Order.advance` |
| ✅ history of state changes | `Order.advance` |
| ✅ snapshot / restore | `Order.snapshot` |
| ✅ lifecycle: context manager and close | `Order.__exit__` |
| ✅ lifecycle: finalizer on garbage collection | `Order.__init__` |

## Key learnings
- Every instance owns its state; class variables track facts about all instances.
- A transition table makes illegal state changes impossible to perform by accident.
- Context managers and `weakref.finalize` give objects a predictable end of life.

## Pitfalls I hit (and how I fixed them)
- Negative damage used to heal a player above max HP; state changes now go through validated methods.

## Run it
```bash
./propython.sh 36                 # study mode: explanation, code map, notes and tests
python -m src.day_36_python_instances_and_state.main
pytest tests/test_day_36.py -v
```

## Next step
- Formalise `__enter__`/`__exit__` on Day 68.
