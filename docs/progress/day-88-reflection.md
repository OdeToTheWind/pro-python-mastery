# Day 88 – Automated Report Generator Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_88_automated_report_generator/main.py`](../../src/day_88_automated_report_generator/main.py) · **Tests:** [`tests/test_day_88.py`](../../tests/test_day_88.py) (8 tests)

## Scenario
A *freelance design studio's month-end report*. Time-tracking entries are aggregated per client and project with exact ``Decimal`` money, then rendered three ways: an HTML e-mail body from ``string.Template`` (auto-escaped), a CSV for the accountant, and a one-page PDF written by hand – no third-party PDF library needed.

## Syllabus deliverables
> Data aggregation, string.Template or Jinja2, and PDF/CSV output

| Deliverable | Implemented in |
|---|---|
| ✅ aggregation by client and project | `aggregate` |
| ✅ string.Template rendering | `render_html` |
| ✅ CSV export | `to_csv` |
| ✅ PDF export | `to_pdf` |
| ✅ one-call report build | `build_reports` |

## Key learnings
- Aggregate with `Decimal` and round once per line, never per entry, to keep totals exact.
- `string.Template.substitute` fails loudly on a missing field; every value is HTML-escaped first.
- A valid PDF is just objects plus a byte-exact cross-reference table – no library needed for simple pages.

## Pitfalls I hit (and how I fixed them)
- CSV cells starting with `=`, `+`, `-` or `@` run as spreadsheet formulas – prefix them to neutralise injection.

## Run it
```bash
./propython.sh 88                 # study mode: explanation, code map, notes and tests
python -m src.day_88_automated_report_generator.main
pytest tests/test_day_88.py -v
```

## Next step
- Run background jobs on a schedule on Day 89.
