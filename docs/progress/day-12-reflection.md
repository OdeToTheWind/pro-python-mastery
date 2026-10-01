# Day 12 – Functions Reflection

**Date:** 2026-03-24 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_12_functions/main.py`](../../src/day_12_functions/main.py) · **Tests:** [`tests/test_day_12.py`](../../tests/test_day_12.py) (9 tests)

## Scenario
A *coffee-shop ordering system* built from small, documented, type-hinted functions.

## Syllabus deliverables
> Parameters, default arguments, \*args, \*\*kwargs, docstrings, type hints

| Deliverable | Implemented in |
|---|---|
| ✅ parameters | `price_drink` |
| ✅ default arguments | `price_drink` |
| ✅ \*args | `order_total` |
| ✅ \*\*kwargs | `customize` |
| ✅ docstrings | `price_drink` |
| ✅ type hints | `Drink` |

## Key learnings
- Defaults are evaluated once; immutable defaults are safe, mutable ones are not.
- `*drinks` collects positional arguments into a tuple; `**extras` collects keywords into a dict.
- Google-style docstrings with Args/Returns/Raises make `help()` genuinely useful.

## Pitfalls I hit (and how I fixed them)
- Unknown keyword extras were silently accepted – they are now rejected with a clear message.

## Run it
```bash
python -m src.day_12_functions.main
pytest tests/test_day_12.py -v
```

## Next step
- Study every parameter kind and ordering rule on Day 34.
