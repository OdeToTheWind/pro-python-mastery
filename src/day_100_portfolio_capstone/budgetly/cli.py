"""Command-line interface: argparse subcommands, logging to stderr, exit codes."""

from __future__ import annotations

import argparse
import logging
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from . import __version__
from .config import Config, load_config
from .models import CATEGORIES, BudgetError, Expense, parse_amount
from .reports import render_table, summarise, to_csv
from .storage import open_store

log = logging.getLogger("budgetly")


def month_arg(text: str) -> tuple[int, int]:
    try:
        year, month = map(int, text.split("-"))
        date(year, month, 1)
    except ValueError:
        raise argparse.ArgumentTypeError(f"expected YYYY-MM, got {text!r}") from None
    return year, month


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="budgetly", description="Track spending against monthly budgets.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--config", type=Path, help="TOML config file")
    parser.add_argument("-v", "--verbose", action="store_true", help="log progress to stderr")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="record an expense")
    add.add_argument("amount", type=str)
    add.add_argument("category", choices=CATEGORIES)
    add.add_argument("note", nargs="?", default="")
    add.add_argument("--on", type=date.fromisoformat, default=None, help="date (YYYY-MM-DD, default today)")
    for name in ("list", "report", "export"):
        cmd = sub.add_parser(name, help=f"{name} one month")
        cmd.add_argument("month", type=month_arg, nargs="?", default=None, help="YYYY-MM (default this month)")
    rm = sub.add_parser("delete", help="delete an expense by id")
    rm.add_argument("id", type=int)
    return parser


def execute(args: argparse.Namespace, config: Config, today: date) -> str:
    with open_store(config.db_path) as store:
        if args.command == "add":
            expense = Expense(args.on or today, parse_amount(args.amount), args.category, args.note)
            if expense.spent_on > today:
                raise BudgetError("expenses cannot be in the future")
            return f"added #{store.add(expense)}: {expense.amount} {config.currency} {expense.category}"
        if args.command == "delete":
            if not store.delete(args.id):
                raise BudgetError(f"no expense #{args.id}")
            return f"deleted #{args.id}"
        year, month = args.month or (today.year, today.month)
        expenses = store.month(year, month)
        if args.command == "list":
            return "\n".join(f"#{e.id} {e.spent_on} {e.amount:>9} {e.category:<10} {e.note}"
                             for e in expenses) or "no expenses yet"
        if args.command == "export":
            return to_csv(expenses).rstrip("\n")
        return render_table(summarise(expenses, config.budgets), config.currency)


def main(argv: Sequence[str] | None = None, *, env: dict[str, str] | None = None, today: date | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code or 0)
    try:
        config = load_config(args.config, env)
        logging.basicConfig(level="INFO" if args.verbose else config.log_level, stream=sys.stderr,
                            format="%(levelname)s %(name)s: %(message)s", force=True)
        print(execute(args, config, today or date.today()))
        return 0
    except BudgetError as exc:
        print(f"budgetly: {exc}", file=sys.stderr)
        return 1
