# Day 83 – Robust CLI Application Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_83_robust_cli_application/main.py`](../../src/day_83_robust_cli_application/main.py) · **Tests:** [`tests/test_day_83.py`](../../tests/test_day_83.py) (13 tests)

## Scenario
``habits`` – a *habit-tracker command-line app* with subcommands (``add``, ``done``, ``list``, ``streak``, ``config``), a TOML config file plus environment overrides, logging controlled by ``-v``/``-q``, JSON output for scripting, and proper exit codes.

## Syllabus deliverables
> argparse or click/typer, subcommands, configuration, and logging

| Deliverable | Implemented in |
|---|---|
| ✅ argparse parser with subcommands | `build_parser` |
| ✅ argument types and validation | `parse_day` |
| ✅ layered configuration | `load_config` |
| ✅ logging with -v / -q | `setup_logging` |
| ✅ exit codes | `EXIT_CODES` |
| ✅ atomic storage | `HabitStore.save` |
| ✅ entry point | `run` |

## Key learnings
- argparse subcommands, `type=` converters and mutually exclusive groups validate input before any logic runs.
- Configuration layers (defaults < file < environment < flags) keep behaviour predictable.
- Logs go to stderr and data to stdout, so the tool stays scriptable; exit codes tell scripts what happened.

## Pitfalls I hit (and how I fixed them)
- Calling `sys.exit` deep inside the code makes it untestable – return an exit code from `run()` instead.

## Run it
```bash
./propython.sh 83                 # study mode: explanation, code map, notes and tests
python -m src.day_83_robust_cli_application.main
pytest tests/test_day_83.py -v
```

## Next step
- Stream files through an ETL pipeline on Day 84.
