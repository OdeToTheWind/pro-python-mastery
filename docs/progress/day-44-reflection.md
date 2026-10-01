# Day 44 – Introduction to the Pandas Framework Reflection

**Date:** 2026-04-25 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_44_pandas_framework/main.py`](../../src/day_44_pandas_framework/main.py) · **Tests:** [`tests/test_day_44.py`](../../tests/test_day_44.py) (7 tests)

## Scenario
A *coffee-chain sales analysis* – load a CSV into a DataFrame, clean it, add derived columns and answer business questions.

## Syllabus deliverables
> DataFrames, data analysis basics with pandas

| Deliverable | Implemented in |
|---|---|
| ✅ creating a DataFrame from CSV | `load_sales` |
| ✅ cleaning (missing values, types) | `load_sales` |
| ✅ derived columns | `load_sales` |
| ✅ selection with loc / iloc and boolean masks | `best_days` |
| ✅ groupby aggregation | `revenue_by_store` |
| ✅ pivot table | `monthly_pivot` |
| ✅ summary statistics | `summary` |

## Key learnings
- `read_csv` + `fillna` + `astype` is the typical load-and-clean sequence.
- Boolean masks with `.loc` select rows and columns in one step.
- `groupby` and `pivot_table` answer most business questions in a line.

## Pitfalls I hit (and how I fixed them)
- `pandas` was missing from `requirements.txt`, which broke CI collection.

## Run it
```bash
python -m src.day_44_pandas_framework.main
pytest tests/test_day_44.py -v
```

## Next step
- Profile pandas vs pure Python on Day 80.
