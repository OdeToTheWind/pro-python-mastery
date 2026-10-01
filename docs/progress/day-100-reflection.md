# Day 100 – Portfolio Capstone: Production-ready Python Tool Reflection

**Date:** 2026-10-01 · **Level:** Capstone · **Python:** 3.12+ · **Status:** Covered
**Code:** [`src/day_100_portfolio_capstone/main.py`](../../src/day_100_portfolio_capstone/main.py) · **Tests:** [`tests/test_day_100.py`](../../tests/test_day_100.py) (12 tests)

## Scenario
``budgetly`` – a *personal expense tracker* you could put on your CV. Five focused modules (models, config, storage, reports, cli) give a command-line tool with layered configuration, SQLite storage with schema migrations, logging, exit codes, CSV export, a ``pyproject.toml`` with a console script, a README, and a test suite holding the package above 90 % branch coverage.

## Syllabus deliverables
> A useful multi-module tool with CLI, tests (>90% coverage), logging, config, packaging, and docs

| Deliverable | Implemented in |
|---|---|
| ✅ CLI entry point | `cli.main` |
| ✅ validated domain model | `models.Expense` |
| ✅ layered configuration | `config.load_config` |
| ✅ SQLite storage with migrations | `storage.Store.migrate` |
| ✅ reports and CSV export | `reports.summarise` |
| ✅ packaging metadata | `PYPROJECT` |
| ✅ documentation | `README` |
| ✅ coverage gate | `COVERAGE_COMMAND` |

## Key learnings
- A production-style tool is small, focused modules: models, config, storage, reports and the CLI.
- Layered configuration, SQLite migrations, logging, exit codes and packaging fit together into one product.
- A branch-coverage gate above 90 % keeps the tool safe to change.

## Pitfalls I hit (and how I fixed them)
- Mixing CLI parsing with business logic makes both hard to test – keep the logic in pure functions.

## Run it
```bash
python -m src.day_100_portfolio_capstone.main
pytest tests/test_day_100.py -v
```

## Next step
- Course complete – continue with the roadmap in learning_develop.md.
