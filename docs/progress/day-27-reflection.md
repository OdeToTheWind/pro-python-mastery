# Day 27 – Python Object Oriented Programming Reflection

**Date:** 2026-04-08 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_27_oop_basics/main.py`](../../src/day_27_oop_basics/main.py) · **Tests:** [`tests/test_day_27.py`](../../tests/test_day_27.py) (9 tests)

## Scenario
A *payment gateway* that accepts several payment methods through one abstract interface while hiding sensitive card data.

## Syllabus deliverables
> OOP fundamentals, classes, objects, encapsulation and abstraction

| Deliverable | Implemented in |
|---|---|
| ✅ classes and objects | `Wallet` |
| ✅ encapsulation | `CreditCard` |
| ✅ abstraction | `PaymentMethod` |
| ✅ polymorphism | `checkout` |

## Key learnings
- Abstract base classes define a contract; Python refuses to instantiate an incomplete subclass.
- Encapsulation in Python is convention (`_x`) plus name mangling (`__x`) plus read-only properties.
- Polymorphism lets `checkout()` work with any payment method without type checks.

## Pitfalls I hit (and how I fixed them)
- `__repr__` must never reveal card numbers – it shows a masked version instead.

## Run it
```bash
./propython.sh 27                 # study mode: explanation, code map, notes and tests
python -m src.day_27_oop_basics.main
pytest tests/test_day_27.py -v
```

## Next step
- Explore `typing.Protocol` (structural typing) on Day 72.
