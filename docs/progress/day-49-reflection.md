# Day 49 – Strongly Dynamic Typing Reflection

**Date:** 2026-04-30 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_49_strongly_dynamic_typing/main.py`](../../src/day_49_strongly_dynamic_typing/main.py) · **Tests:** [`tests/test_day_49.py`](../../tests/test_day_49.py) (8 tests)

## Scenario
A *product-import pipeline* receiving loosely typed data from spreadsheets and APIs. Python is **dynamic** (names can be rebound to any type at runtime) but **strong** (it refuses to silently mix incompatible types).

## Syllabus deliverables
> Python's dynamic typing behaviour and practical implications

| Deliverable | Implemented in |
|---|---|
| ✅ dynamic typing (rebinding) | `rebinding_demo` |
| ✅ strong typing (no implicit coercion) | `strong_typing_errors` |
| ✅ explicit conversion | `add_quantities` |
| ✅ duck typing | `total_length` |
| ✅ hints are not enforced at runtime | `hints_not_enforced` |
| ✅ opt-in runtime enforcement | `enforce_types` |

## Key learnings
- Dynamic: a name can hold any type over time. Strong: Python won't implicitly mix incompatible types.
- Duck typing asks 'can it do this?' rather than 'what class is it?'.
- Type hints are checked by tools such as mypy, not by the interpreter.

## Pitfalls I hit (and how I fixed them)
- `True + 1 == 2` because `bool` subclasses `int` – an edge case of strong typing.

## Run it
```bash
./propython.sh 49                 # study mode: explanation, code map, notes and tests
python -m src.day_49_strongly_dynamic_typing.main
pytest tests/test_day_49.py -v
```

## Next step
- Go further with `Protocol`, generics and mypy on Day 72.
