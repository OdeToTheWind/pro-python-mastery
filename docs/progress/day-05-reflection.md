# Day 05 – Mathematical Operations Reflection

**Date:** 2026-03-17 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_05_math_operations/main.py`](../../src/day_05_math_operations/main.py) · **Tests:** [`tests/test_day_05.py`](../../tests/test_day_05.py) (12 tests)

## Scenario
A *restaurant bill splitter* – arithmetic with money, where rounding, floor division and division by zero all matter.

## Syllabus deliverables
> Arithmetic operators, precedence, floor division, safe division handling

| Deliverable | Implemented in |
|---|---|
| ✅ arithmetic operators | `calculate` |
| ✅ operator precedence | `precedence_examples` |
| ✅ floor division and modulo with negatives | `floor_division_facts` |
| ✅ safe division | `safe_divide` |
| ✅ practical application (bill splitting) | `split_bill` |

## Key learnings
- `//` floors towards negative infinity, so `-7 // 2 == -4` while `int(-7 / 2) == -3`.
- `divmod` keeps `a == b * q + r` true for every sign combination.
- Money belongs in `Decimal` with integer cents; floats cannot split €100 three ways exactly.

## Pitfalls I hit (and how I fixed them)
- Returning the string `"Error"` from a numeric function mixed types – the function now raises.
- `10.0 ** 1000` raises `OverflowError`, which the calculator now reports instead of crashing.

## Run it
```bash
python -m src.day_05_math_operations.main
pytest tests/test_day_05.py -v
```

## Next step
- Profile `Decimal` vs `float` on Day 80 to see the performance trade-off.
