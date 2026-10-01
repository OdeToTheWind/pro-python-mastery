# Day 50 – Error Handling and Exceptions Reflection

**Date:** 2026-05-01 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_50_error_handling_exceptions/main.py`](../../src/day_50_error_handling_exceptions/main.py) · **Tests:** [`tests/test_day_50.py`](../../tests/test_day_50.py) (13 tests)

## Scenario
A *configuration loader for a microservice* that reads JSON from disk, validates many fields at once, retries flaky reads and logs failures with full context.

## Syllabus deliverables
> Advanced exception handling techniques and best practices

| Deliverable | Implemented in |
|---|---|
| ✅ exception chaining (raise from) | `parse_config` |
| ✅ add\_note() for extra context | `parse_config` |
| ✅ ExceptionGroup for multiple errors | `validate_config` |
| ✅ except\* to handle groups by type | `load_service_config` |
| ✅ retry with backoff | `retry` |
| ✅ contextlib.suppress | `remove_stale_lock` |
| ✅ logging.exception best practice | `load_service_config` |

## Key learnings
- `raise X from exc` keeps the original error as `__cause__` for debugging.
- `ExceptionGroup` reports many validation problems at once; `except*` handles each kind.
- Retry only transient errors, with backoff, and re-raise the last one.

## Pitfalls I hit (and how I fixed them)
- `logging.exception` records the traceback; printing `str(exc)` loses it.

## Run it
```bash
python -m src.day_50_error_handling_exceptions.main
pytest tests/test_day_50.py -v
```

## Next step
- Structured logging and log rotation come on Days 77 and 86.
