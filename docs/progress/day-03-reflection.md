# Day 03 – Input & Print Functions Reflection

**Date:** 2026-03-15 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_03_input_output/main.py`](../../src/day_03_input_output/main.py) · **Tests:** [`tests/test_day_03.py`](../../tests/test_day_03.py) (11 tests)

## Scenario
A *workshop registration desk* that asks attendees questions in the console, validates every answer and prints a receipt.

## Syllabus deliverables
> User input validation, type conversion, interactive console applications

| Deliverable | Implemented in |
|---|---|
| ✅ input validation | `ask` |
| ✅ type conversion | `to_int_in_range` |
| ✅ interactive console application | `register` |
| ✅ formatted print output | `format_receipt` |

## Key learnings
- Inject `ask`/`print` callables so an interactive program can be tested without a keyboard.
- `EOFError` is how Ctrl-D or a closed pipe looks to `input()` – it must end the conversation, not be retried.
- Convert and validate in one small function per field; the prompt loop stays generic.

## Pitfalls I hit (and how I fixed them)
- A broad `except Exception` retried forever on EOF – catching only `ValueError` fixed it.

## Run it
```bash
./propython.sh 3                 # study mode: explanation, code map, notes and tests
python -m src.day_03_input_output.main
pytest tests/test_day_03.py -v
```

## Next step
- Reuse the `ask()` pattern for every console menu in later days.
