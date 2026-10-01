# budgetly

Track spending against monthly budgets from the terminal. It is the Day 100 portfolio capstone of Pro Python Mastery.

```bash
budgetly add 12,50 food "lunch with Sam"
budgetly report 2026-09
budgetly export 2026-09 > september.csv
```

## Configuration

Settings are layered as defaults, then the TOML file passed with `--config`, then environment variables. Each layer overrides the one before it.

```toml
db_path = "~/budget.db"
currency = "EUR"

[budgets]
food = 400
fun = 120
```

You can also set these environment variables:

- `BUDGETLY_DB`: path to the database file.
- `BUDGETLY_LOG_LEVEL`: one of `DEBUG`, `INFO`, `WARNING` or `ERROR`.

## Design

| Module | Responsibility |
|---|---|
| `models.py` | Validated domain objects, with money held as `Decimal` |
| `config.py` | Layered configuration |
| `storage.py` | SQLite with migrations and parameterised SQL |
| `reports.py` | Pure functions for summaries, tables and CSV |
| `cli.py` | argparse, logging and exit codes |

## Development

```bash
pytest tests/test_day_100.py --cov=src/day_100_portfolio_capstone/budgetly --cov-branch --cov-fail-under=90
```
