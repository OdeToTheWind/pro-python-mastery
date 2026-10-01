# Day 91 – Type-safe Configuration System Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_91_type_safe_configuration/main.py`](../../src/day_91_type_safe_configuration/main.py) · **Tests:** [`tests/test_day_91.py`](../../tests/test_day_91.py) (10 tests)

## Scenario
An *IoT fleet firmware-rollout service*. Its settings are frozen dataclasses whose **type hints drive parsing**: environment variables such as ``FLEET_DB__PORT=5433`` or ``FLEET_ROLLOUT__REGIONS=eu,us`` are coerced to ``int``, ``bool``, ``Path``, ``Literal``, ``Enum``, tuples and secrets, every problem is reported at once, and secrets never appear in logs.

## Syllabus deliverables
> Pydantic or dataclasses, validation, and environment variables

| Deliverable | Implemented in |
|---|---|
| ✅ typed settings schema | `Settings` |
| ✅ secret values that mask themselves | `Secret` |
| ✅ type-hint driven coercion | `coerce` |
| ✅ load from environment variables | `load_settings` |
| ✅ all errors reported together | `ConfigError` |
| ✅ cross-field validation | `Settings.__post_init__` |
| ✅ generated documentation | `describe` |
| ✅ safe dump for logs | `safe_dict` |

## Key learnings
- Type hints can drive parsing: one `coerce` function turns strings into int, bool, Path, Literal, Enum or tuples.
- Collecting every problem before raising lets operators fix a configuration in one pass.
- A `Secret` type whose repr is masked keeps passwords out of logs and tracebacks.

## Pitfalls I hit (and how I fixed them)
- A typo in an environment variable name is silently ignored unless unknown keys are reported.

## Run it
```bash
./propython.sh 91                 # study mode: explanation, code map, notes and tests
python -m src.day_91_type_safe_configuration.main
pytest tests/test_day_91.py -v
```

## Next step
- Write a full test suite for a multi-module package on Day 92.
