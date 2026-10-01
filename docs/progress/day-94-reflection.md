# Day 94 – Data Validation & Cleaning Library Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_94_data_validation_library/main.py`](../../src/day_94_data_validation_library/main.py) · **Tests:** [`tests/test_day_94.py`](../../tests/test_day_94.py) (11 tests)

## Scenario
``intake`` – a reusable validation library for a *clinical-trial patient intake* system. Messy form data ("72,5 kg", " F ", "1980/03/07") is cleaned and validated by small composable, type-hinted validators; every error carries its exact path (``visits[1].date``) so a coordinator can fix the whole form in one go.

## Syllabus deliverables
> Reusable validators, custom exceptions, and type hints

| Deliverable | Implemented in |
|---|---|
| ✅ generic composable validator | `Validator` |
| ✅ string / number / date / choice validators | `text` |
| ✅ list and nested schema validators | `schema` |
| ✅ custom exception with field path | `ValidationError` |
| ✅ aggregated schema errors | `SchemaError` |
| ✅ cleaning helpers | `parse_measurement` |
| ✅ batch validation report | `validate_batch` |

## Key learnings
- Small generic `Validator[T]` objects compose with `>>`, `optional()` and `default()`.
- Errors that carry a path (`visits[1].date`) tell users exactly what to fix.
- Cleaning (whitespace, decimal commas, units) belongs in the validator, before checking the rules.

## Pitfalls I hit (and how I fixed them)
- Stopping at the first error forces users through many frustrating round-trips.

## Run it
```bash
python -m src.day_94_data_validation_library.main
pytest tests/test_day_94.py -v
```

## Next step
- Optimise a performance-critical module on Day 95.
