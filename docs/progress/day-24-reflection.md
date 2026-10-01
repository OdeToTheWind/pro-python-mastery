# Day 24 – Debugging Techniques Reflection

**Date:** 2026-04-05 · **Level:** Beginner · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_24_debugging_techniques/main.py`](../../src/day_24_debugging_techniques/main.py) · **Tests:** [`tests/test_day_24.py`](../../tests/test_day_24.py) (9 tests)

## Scenario
A *payroll script* that ships with a real bug. We find it with print debugging, read its traceback, set a (switchable) breakpoint, and locate the first failing input systematically.

## Syllabus deliverables
> Print debugging, tracebacks, breakpoints, and systematic bug fixing

| Deliverable | Implemented in |
|---|---|
| ✅ print debugging (switchable trace) | `trace_calls` |
| ✅ reading tracebacks | `summarize_traceback` |
| ✅ breakpoints | `maybe_breakpoint` |
| ✅ systematic isolation of failing input | `first_failing_input` |
| ✅ bug and its fix side by side | `net_pay_fixed` |

## Key learnings
- Read a traceback bottom-up: the last line names the exception, the frame above it shows where.
- Debug output goes to stderr behind a switch, never mixed into real output.
- `breakpoint()` respects `PYTHONBREAKPOINT=0`, so breakpoints can stay in code safely.

## Pitfalls I hit (and how I fixed them)
- Isolating the *first* failing input (an empty week) found the bug faster than reading code.

## Run it
```bash
./propython.sh 24                 # study mode: explanation, code map, notes and tests
python -m src.day_24_debugging_techniques.main
pytest tests/test_day_24.py -v
```

## Next step
- Build a full observability toolkit on Day 99.
