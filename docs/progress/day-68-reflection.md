# Day 68 – Context Managers Reflection

**Date:** 2026-10-01 · **Level:** Advanced · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_68_context_managers/main.py`](../../src/day_68_context_managers/main.py) · **Tests:** [`tests/test_day_68.py`](../../tests/test_day_68.py) (11 tests)

## Scenario
A *laboratory experiment runner*. Instruments must always be switched off, partial results rolled back on failure, and timings recorded – even when an experiment crashes halfway.

## Syllabus deliverables
> The with statement, \_\_enter\_\_, \_\_exit\_\_, and contextlib

| Deliverable | Implemented in |
|---|---|
| ✅ class-based context manager (\_\_enter\_\_/\_\_exit\_\_) | `Instrument` |
| ✅ transaction with rollback in \_\_exit\_\_ | `ResultsLog.transaction` |
| ✅ suppressing a specific exception | `IgnoreCalibrationWarnings` |
| ✅ @contextmanager generator | `timer` |
| ✅ ExitStack for a dynamic number of resources | `run_experiment` |
| ✅ contextlib.suppress / redirect\_stdout / nullcontext / chdir | `capture_output` |

## Key learnings
- `__exit__` always runs; returning a truthy value suppresses the exception, so only do it deliberately.
- `@contextmanager` turns a generator into a context manager: code before `yield` is enter, `finally` is exit.
- `ExitStack` manages a dynamic number of resources and releases them in reverse order, even if one fails to start.

## Pitfalls I hit (and how I fixed them)
- A transaction must roll back staged rows *and* re-raise – swallowing the error would hide the failed experiment.

## Run it
```bash
python -m src.day_68_context_managers.main
pytest tests/test_day_68.py -v
```

## Next step
- See the descriptor protocol that powers `@property` on Day 69.
