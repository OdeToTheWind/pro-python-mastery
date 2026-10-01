"""Tests for Day 100 – budgetly, the portfolio capstone (package coverage > 90 %)."""

import csv
import io
import logging
import sqlite3
import tomllib
from datetime import date
from decimal import Decimal

import pytest

from src.day_100_portfolio_capstone.budgetly import __version__
from src.day_100_portfolio_capstone.budgetly.cli import main as cli
from src.day_100_portfolio_capstone.budgetly.config import load_config
from src.day_100_portfolio_capstone.budgetly.models import BudgetError, Expense, parse_amount
from src.day_100_portfolio_capstone.budgetly.reports import render_table, summarise, to_csv
from src.day_100_portfolio_capstone.budgetly.storage import MIGRATIONS, open_store
from src.day_100_portfolio_capstone.main import COVERAGE_COMMAND, PYPROJECT, README, main

TODAY = date(2026, 9, 30)


@pytest.fixture
def env(tmp_path):
    return {"BUDGETLY_DB": str(tmp_path / "data" / "budget.db")}


@pytest.fixture
def run(env, capsys):
    def invoke(*argv, today=TODAY):
        code = cli(list(argv), env=env, today=today)
        out = capsys.readouterr()
        return code, out.out.strip(), out.err.strip()

    return invoke


@pytest.mark.parametrize(("text", "value"), [("12,5", "12.50"), ("0.01", "0.01"), ("3.456", "3.46")])
def test_parse_amount(text, value):
    assert parse_amount(text) == Decimal(value)


@pytest.mark.parametrize(("text", "message"), [("abc", "not an amount"), ("0", "between"), ("-3", "between"),
                                               ("2000000", "between")])
def test_parse_amount_rejects(text, message):
    with pytest.raises(BudgetError, match=message):
        parse_amount(text)


def test_expense_validation():
    with pytest.raises(BudgetError, match="unknown category"):
        Expense(TODAY, Decimal(1), "yachts")
    with pytest.raises(BudgetError, match="120"):
        Expense(TODAY, Decimal(1), "food", "x" * 121)


def test_config_layers(tmp_path):
    cfg = tmp_path / "c.toml"
    cfg.write_text('db_path = "~/b.db"\ncurrency = "GBP"\n[budgets]\nfood = 400.5\n', encoding="utf-8")
    loaded = load_config(cfg, env={})
    assert loaded.currency == "GBP" and loaded.budgets == {"food": Decimal("400.5")}
    assert loaded.db_path.name == "b.db" and "~" not in str(loaded.db_path)
    overridden = load_config(cfg, env={"BUDGETLY_DB": "/x/y.db", "BUDGETLY_LOG_LEVEL": "debug"})
    assert str(overridden.db_path) == "/x/y.db" and overridden.log_level == "DEBUG"
    assert load_config(None, env={}).currency == "EUR"


@pytest.mark.parametrize(("content", "env", "message"),
                         [(None, {}, "does not exist"), ("x = [", {}, "invalid"),
                          ("[budgets]\nyachts = 1\n", {}, "unknown categories: yachts"),
                          ("", {"BUDGETLY_LOG_LEVEL": "LOUD"}, "invalid BUDGETLY_LOG_LEVEL")])
def test_config_errors(tmp_path, content, env, message):
    cfg = tmp_path / "c.toml"
    if content is not None:
        cfg.write_text(content, encoding="utf-8")
    with pytest.raises(BudgetError, match=message):
        load_config(cfg, env=env)


def test_storage_migrations_and_queries(tmp_path):
    path = tmp_path / "s.db"
    with open_store(path) as store:
        first = store.add(Expense(date(2026, 9, 2), Decimal("9.99"), "fun", "cinema"))
        store.add(Expense(date(2026, 10, 1), Decimal("5"), "food"))
        assert store.migrate() == len(MIGRATIONS)
    with open_store(path) as store:  # reopen: nothing re-applied, data kept
        assert [e.amount for e in store.month(2026, 9)] == [Decimal("9.99")]
        assert store.month(2026, 9)[0].id == first and store.delete(first) and not store.delete(first)
    conn = sqlite3.connect(path)
    assert conn.execute("PRAGMA user_version").fetchone()[0] == 2
    conn.close()
    with open_store(":memory:") as memory:
        assert memory.month(2026, 1) == []


def test_reports_and_csv():
    expenses = [Expense(date(2026, 9, 1), Decimal("30"), "food", "=SUM(A1)", 1),
                Expense(date(2026, 9, 2), Decimal("25.5"), "food", "", 2),
                Expense(date(2026, 9, 3), Decimal("10"), "fun", "", 3)]
    lines = summarise(expenses, {"food": Decimal("50"), "rent": Decimal("700")})
    assert [(ln.category, ln.spent, ln.over_budget) for ln in lines] == [
        ("food", Decimal("55.5"), True), ("fun", Decimal("10"), False), ("rent", Decimal("0"), False)]
    table = render_table(lines, "EUR")
    assert "⚠ over" in table and table.endswith("total           65.50 EUR") and render_table([], "EUR") == "no expenses yet"
    rows = list(csv.reader(io.StringIO(to_csv(expenses))))
    assert rows[0] == ["id", "date", "amount", "category", "note"] and rows[1][4] == "'=SUM(A1)"


def test_cli_workflow(run, tmp_path):
    assert run("add", "12,50", "food", "lunch", "--on", "2026-09-05")[1] == "added #1: 12.50 EUR food"
    run("add", "40", "fun")
    code, out, _ = run("list", "2026-09")
    assert code == 0 and out.splitlines()[0].startswith("#1 2026-09-05     12.50 food")
    assert "total           52.50 EUR" in run("report")[1]
    assert run("export", "2026-09")[1].count("\n") == 2
    assert run("delete", "2")[1] == "deleted #2" and run("list", "2026-08")[1] == "no expenses yet"


@pytest.mark.parametrize(("argv", "code", "message"),
                         [(["add", "abc", "food"], 1, "not an amount"),
                          (["add", "5", "food", "--on", "2026-12-24"], 1, "future"),
                          (["delete", "99"], 1, "no expense #99"),
                          (["add", "5", "yachts"], 2, "invalid choice"),
                          (["report", "2026-13"], 2, "expected YYYY-MM"),
                          (["--config", "/nope.toml", "list"], 1, "does not exist")])
def test_cli_errors(run, argv, code, message):
    result, _out, err = run(*argv)
    assert result == code and message in err


def test_cli_version_and_verbose_logging(run, capsys):
    assert run("--version")[1] == f"budgetly {__version__}"
    code, _out, err = run("-v", "add", "3", "health")
    assert code == 0 and "INFO budgetly.storage: stored expense 1" in err
    logging.getLogger().handlers.clear()


def test_packaging_docs_and_coverage_gate():
    meta = tomllib.loads(PYPROJECT)
    assert meta["project"]["scripts"] == {"budgetly": "budgetly.cli:main"}
    assert meta["project"]["version"] == __version__ and "--cov-fail-under=90" in COVERAGE_COMMAND
    text = README.read_text(encoding="utf-8")
    assert "BUDGETLY_DB" in text and "## Design" in text


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "⚠ over" in out and "(exit 1)" in out and "total           71.50 EUR" in out
