# Day 84 – Data Pipeline / ETL Script Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_84_data_pipeline_etl/main.py`](../../src/day_84_data_pipeline_etl/main.py) · **Tests:** [`tests/test_day_84.py`](../../tests/test_day_84.py) (8 tests)

## Scenario
A *city air-quality ETL*. Sensor stations drop CSV and JSON-lines files into an inbox folder; the pipeline extracts records lazily, transforms and validates them, quarantines bad rows with reasons, loads clean data into JSON-lines output, and writes a run summary – logging every step.

## Syllabus deliverables
> Generators, pathlib, CSV/JSON, error handling, and logging

| Deliverable | Implemented in |
|---|---|
| ✅ extract: discover files with pathlib | `discover` |
| ✅ extract: stream CSV and JSON-lines | `extract` |
| ✅ transform: normalise and validate | `transform` |
| ✅ quarantine bad rows with reasons | `RunStats` |
| ✅ load: write JSON-lines | `load` |
| ✅ summary report | `summarise` |
| ✅ orchestration + logging | `run_pipeline` |

## Key learnings
- Generator stages (extract → transform → load) process any amount of data in one streaming pass.
- Bad rows are quarantined with a reason instead of crashing the run or vanishing silently.
- Writing to a temp file and renaming makes the output atomic for downstream consumers.

## Pitfalls I hit (and how I fixed them)
- Counting statistics inside lazy generators only works once the stream has actually been consumed.

## Run it
```bash
./propython.sh 84                 # study mode: explanation, code map, notes and tests
python -m src.day_84_data_pipeline_etl.main
pytest tests/test_day_84.py -v
```

## Next step
- Combine threads, processes and asyncio in one processor on Day 85.
