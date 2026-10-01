"""Day 100 – Portfolio Capstone: Production-ready Python Tool.

Scenario: ``budgetly`` – a *personal expense tracker* you could put on your
CV. Five focused modules (models, config, storage, reports, cli) give a
command-line tool with layered configuration, SQLite storage with schema
migrations, logging, exit codes, CSV export, a ``pyproject.toml`` with a
console script, a README, and a test suite holding the package above 90 %
branch coverage.

Deliverables (syllabus):
* A useful multi-module tool with a CLI (``budgetly add/list/report/export/delete``)
* Tests with >90 % coverage (``tests/test_day_100.py``, branch coverage gate)
* Logging (stderr, ``-v`` / ``BUDGETLY_LOG_LEVEL``) and configuration (TOML + env)
* Packaging (``PYPROJECT`` with a console-script entry point) and docs (``README.md``)
"""

from __future__ import annotations

import tempfile
from datetime import date
from pathlib import Path

from .budgetly import __version__, cli, config, models, reports, storage

DELIVERABLES: dict[str, str] = {
    "CLI entry point": "cli.main",
    "validated domain model": "models.Expense",
    "layered configuration": "config.load_config",
    "SQLite storage with migrations": "storage.Store.migrate",
    "reports and CSV export": "reports.summarise",
    "packaging metadata": "PYPROJECT",
    "documentation": "README",
    "coverage gate": "COVERAGE_COMMAND",
}

README = Path(__file__).with_name("README.md")
COVERAGE_COMMAND = ("pytest tests/test_day_100.py --cov=src/day_100_portfolio_capstone/budgetly "
                    "--cov-branch --cov-fail-under=90")
PYPROJECT = f"""[build-system]
requires = ["hatchling>=1.25"]
build-backend = "hatchling.build"

[project]
name = "budgetly"
version = "{__version__}"
description = "Track spending against monthly budgets from the terminal."
readme = "README.md"
requires-python = ">=3.12"
license = "MIT"
dependencies = []

[project.scripts]
budgetly = "budgetly.cli:main"

[tool.coverage.report]
fail_under = 90
"""

__all__ = ["COVERAGE_COMMAND", "DELIVERABLES", "PYPROJECT", "README", "cli", "config", "main", "models",
           "reports", "storage"]


def main() -> None:
    print(f"Day 100 – budgetly {__version__}: the portfolio capstone\n")
    today = date(2026, 9, 30)
    with tempfile.TemporaryDirectory() as tmp:
        cfg = Path(tmp) / "budgetly.toml"
        cfg.write_text('currency = "EUR"\n[budgets]\nfood = 50\nfun = 100\n', encoding="utf-8")
        env = {"BUDGETLY_DB": str(Path(tmp) / "budget.db")}
        for argv in (["add", "32,40", "food", "groceries", "--on", "2026-09-03"],
                     ["add", "24.10", "food", "pizza night", "--on", "2026-09-12"],
                     ["add", "15", "transport", "--on", "2026-09-20"],
                     ["add", "abc", "food"],
                     ["--config", str(cfg), "report", "2026-09"]):
            print("$ budgetly", " ".join(a if "/" not in a else "<config>" for a in argv))
            code = cli.main(argv, env=env, today=today)
            print(f"  (exit {code})")


if __name__ == "__main__":
    main()
