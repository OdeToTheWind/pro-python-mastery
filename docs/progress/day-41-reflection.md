# Day 41 – File I/O - Reading and Writing to Local Files Reflection

**Date:** 2026-04-22 · **Level:** Intermediate · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_41_file_io/main.py`](../../src/day_41_file_io/main.py) · **Tests:** [`tests/test_day_41.py`](../../tests/test_day_41.py) (12 tests)

## Scenario
A *daily journal* stored as a UTF-8 text file – one entry per line.

## Syllabus deliverables
> open(), with statements, and file handling patterns

| Deliverable | Implemented in |
|---|---|
| ✅ open() modes w / a / r / x | `write_entries` |
| ✅ with statement | `append_entry` |
| ✅ streaming line by line | `iter_entries` |
| ✅ EAFP: reading a file that may not exist | `read_entries` |
| ✅ atomic write (temp file + replace) | `atomic_write` |
| ✅ exclusive create (mode 'x') | `create_new` |
| ✅ default data location | `default_journal_path` |

## Key learnings
- Always pass `encoding='utf-8'` and use `with` so files are closed even on errors.
- Write every line with a trailing newline so appends never glue lines together.
- Atomic writes (temp file + `os.replace`) protect data against crashes.

## Pitfalls I hit (and how I fixed them)
- Writing without a newline and then appending produced `firstsecond` – a real data bug.

## Run it
```bash
python -m src.day_41_file_io.main
pytest tests/test_day_41.py -v
```

## Next step
- Stream huge files line by line on Day 90.
