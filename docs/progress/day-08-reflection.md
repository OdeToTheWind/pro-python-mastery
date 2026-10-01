# Day 08 – If / Elif / Else Conditionals Reflection

**Date:** 2026-03-20 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_08_if_else_conditionals/main.py`](../../src/day_08_if_else_conditionals/main.py) · **Tests:** [`tests/test_day_08.py`](../../tests/test_day_08.py) (10 tests)

## Scenario
A *hiking-trip weather advisor* that decides what to pack and whether the hike is safe.

## Syllabus deliverables
> Comparison operators, nested logic, truthy/falsy values, chained conditionals

| Deliverable | Implemented in |
|---|---|
| ✅ comparison operators | `compare` |
| ✅ chained comparisons and elif ladder | `classify_temperature` |
| ✅ nested logic | `hike_decision` |
| ✅ truthy/falsy values | `truthiness` |
| ✅ guarding invalid input (NaN, out of range) | `is_plausible_reading` |

## Key learnings
- Chained comparisons (`0 <= c < 10`) read like maths and evaluate the middle value once.
- NaN compares False with everything, so it silently falls through an `elif` ladder unless guarded.
- Empty containers, `0`, `''` and `None` are falsy – `notes or '(no notes)'` is idiomatic.

## Pitfalls I hit (and how I fixed them)
- Keeping the hike rules inside `main()` made them untestable; now each decision is a pure function.

## Run it
```bash
python -m src.day_08_if_else_conditionals.main
pytest tests/test_day_08.py -v
```

## Next step
- Translate the hike decision into a flowchart on Day 16.
