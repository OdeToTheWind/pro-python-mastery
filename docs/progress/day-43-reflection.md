# Day 43 – Reading and Writing to CSV Reflection

**Date:** 2026-04-24 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_43_reading_writing_csv/main.py`](../../src/day_43_reading_writing_csv/main.py) · **Tests:** [`tests/test_day_43.py`](../../tests/test_day_43.py) (9 tests)

## Scenario
A *household expense tracker* that imports a bank CSV export, validates each row, reports bad rows instead of crashing, and exports a category summary.

## Syllabus deliverables
> CSV processing, tabular data import/export and parsing

| Deliverable | Implemented in |
|---|---|
| ✅ reading CSV into dicts | `parse_expenses` |
| ✅ validation of each row | `parse_row` |
| ✅ writing CSV (DictWriter) | `write_expenses` |
| ✅ export of aggregated data | `export_summary` |
| ✅ dialect (delimiter) detection | `detect_delimiter` |

## Key learnings
- `DictReader`/`DictWriter` map columns by name, so column order can change safely.
- Open CSV files with `newline=''`, as the csv docs require.
- Validate each row and collect errors with line numbers instead of failing the whole import.

## Pitfalls I hit (and how I fixed them)
- The Sniffer guessed quoting rules wrongly from one header line; only the delimiter is sniffed now.

## Run it
```bash
./propython.sh 43                 # study mode: explanation, code map, notes and tests
python -m src.day_43_reading_writing_csv.main
pytest tests/test_day_43.py -v
```

## Next step
- Export reports to CSV in the report generator (Day 88).
