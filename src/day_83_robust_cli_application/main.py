"""Day 83 – Capstone: Robust CLI Application.

Scenario: ``habits`` – a *habit-tracker command-line app* with subcommands
(``add``, ``done``, ``list``, ``streak``, ``config``), a TOML config file plus
environment overrides, logging controlled by ``-v``/``-q``, JSON output for
scripting, and proper exit codes.

Deliverables (syllabus):
* ``argparse`` (subcommands, types, choices, mutually exclusive flags, ``--version``)
* Configuration (defaults < config file < environment < command-line flags)
* Logging (verbosity flags, log to stderr so stdout stays machine-readable)
* Robustness: exit codes, friendly errors, atomic JSON storage
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import tempfile
import tomllib
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any

DELIVERABLES: dict[str, str] = {
    "argparse parser with subcommands": "build_parser",
    "argument types and validation": "parse_day",
    "layered configuration": "load_config",
    "logging with -v / -q": "setup_logging",
    "exit codes": "EXIT_CODES",
    "atomic storage": "HabitStore.save",
    "entry point": "run",
}

__version__ = "1.0.0"
EXIT_CODES = {"ok": 0, "error": 1, "usage": 2, "not_found": 3}
log = logging.getLogger("habits")


class CLIError(Exception):
    def __init__(self, message: str, code: int = EXIT_CODES["error"]) -> None:
        super().__init__(message)
        self.code = code


@dataclass
class Config:
    data_file: Path = field(default_factory=lambda: Path.cwd() / ".data" / "habits.json")
    week_starts_monday: bool = True
    default_format: str = "text"


def load_config(path: Path | None, env: dict[str, str] | None = None) -> Config:
    env = dict(os.environ) if env is None else env
    config = Config()
    if path is not None and path.exists():
        data = tomllib.loads(path.read_text(encoding="utf-8")).get("habits", {})
        if "data_file" in data:
            config.data_file = Path(data["data_file"]).expanduser()
        config.week_starts_monday = bool(data.get("week_starts_monday", config.week_starts_monday))
        config.default_format = str(data.get("default_format", config.default_format))
    if "HABITS_DATA_FILE" in env:
        config.data_file = Path(env["HABITS_DATA_FILE"]).expanduser()
    if config.default_format not in {"text", "json"}:
        raise CLIError(f"invalid default_format {config.default_format!r}", EXIT_CODES["usage"])
    return config


class HabitStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.habits: dict[str, list[str]] = {}
        if path.exists():
            try:
                self.habits = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise CLIError(f"data file {path} is corrupt: {exc}") from exc

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.path.parent, suffix=".tmp")
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(self.habits, handle, indent=2, sort_keys=True)
        os.replace(tmp, self.path)
        log.debug("saved %d habits to %s", len(self.habits), self.path)


def parse_day(text: str) -> date:
    """argparse ``type=``: raise ArgumentTypeError for a clean usage message."""
    if text == "today":
        return date.today()
    if text == "yesterday":
        return date.today() - timedelta(days=1)
    try:
        return date.fromisoformat(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid date {text!r} (use YYYY-MM-DD, today or yesterday)") from None


def habit_name(text: str) -> str:
    name = " ".join(text.split()).lower()
    if not name or len(name) > 40:
        raise argparse.ArgumentTypeError("habit names must be 1–40 characters")
    return name


def streak(days: list[str], today: date) -> int:
    done = {date.fromisoformat(d) for d in days}
    count, current = 0, today if today in done else today - timedelta(days=1)
    while current in done:
        count += 1
        current -= timedelta(days=1)
    return count


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="habits", description="Track daily habits from the terminal.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--config", type=Path, help="TOML config file (section [habits])")
    noise = parser.add_mutually_exclusive_group()
    noise.add_argument("-v", "--verbose", action="count", default=0, help="more logging (-vv for debug)")
    noise.add_argument("-q", "--quiet", action="store_true", help="only errors")
    parser.add_argument("--format", choices=["text", "json"], help="output format")
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")

    add = sub.add_parser("add", help="start tracking a habit")
    add.add_argument("name", type=habit_name)

    done = sub.add_parser("done", help="mark a habit as done")
    done.add_argument("name", type=habit_name)
    done.add_argument("--on", type=parse_day, default="today", help="date (default: today)")

    sub.add_parser("list", help="show habits and streaks")

    st = sub.add_parser("streak", help="current streak of one habit")
    st.add_argument("name", type=habit_name)

    cfg = sub.add_parser("config", help="show the effective configuration")
    cfg.add_argument("--path-only", action="store_true")
    return parser


def setup_logging(verbose: int, quiet: bool) -> None:
    level = logging.ERROR if quiet else [logging.WARNING, logging.INFO, logging.DEBUG][min(verbose, 2)]
    handler = logging.StreamHandler(sys.stderr)  # stdout stays clean for data / JSON
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    log.handlers[:] = [handler]
    log.setLevel(level)
    log.propagate = False


def execute(args: argparse.Namespace, config: Config, today: date) -> Any:
    store = HabitStore(config.data_file)
    if args.command == "config":
        return str(config.data_file) if args.path_only else {k: str(v) for k, v in vars(config).items()}
    if args.command == "add":
        if args.name in store.habits:
            raise CLIError(f"habit {args.name!r} already exists")
        store.habits[args.name] = []
        store.save()
        log.info("added %s", args.name)
        return {"added": args.name}
    if args.command in {"done", "streak"} and args.name not in store.habits:
        raise CLIError(f"no habit called {args.name!r} (try: habits add)", EXIT_CODES["not_found"])
    if args.command == "done":
        if args.on > today:
            raise CLIError("cannot complete a habit in the future", EXIT_CODES["usage"])
        days = store.habits[args.name]
        if args.on.isoformat() not in days:
            days.append(args.on.isoformat())
            days.sort()
            store.save()
        return {"habit": args.name, "streak": streak(days, today)}
    if args.command == "streak":
        return {"habit": args.name, "streak": streak(store.habits[args.name], today)}
    return {name: streak(days, today) for name, days in sorted(store.habits.items())}


def render(result: Any, fmt: str) -> str:
    if fmt == "json":
        return json.dumps(result, sort_keys=True)
    if isinstance(result, dict):
        return "\n".join(f"{k:<20} {v}" for k, v in result.items()) or "(nothing yet)"
    return str(result)


def run(argv: Sequence[str] | None = None, *, env: dict[str, str] | None = None, today: date | None = None) -> int:
    """The console-script entry point: returns an exit code instead of calling sys.exit."""
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:  # argparse exits on --help/--version/usage errors
        return int(exc.code or 0)
    setup_logging(args.verbose, args.quiet)
    try:
        config = load_config(args.config, env)
        result = execute(args, config, today or date.today())
    except CLIError as exc:
        log.error("%s", exc)
        return exc.code
    print(render(result, args.format or config.default_format))
    return EXIT_CODES["ok"]


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        env = {"HABITS_DATA_FILE": str(Path(tmp) / "habits.json")}
        today = date(2026, 10, 1)
        print("Day 83 – habits CLI demo\n")
        for argv in (["add", "Read 20 pages"], ["done", "read 20 pages", "--on", "2026-09-30"],
                     ["done", "read 20 pages"], ["--format", "json", "list"], ["streak", "yoga"]):
            print("$ habits", " ".join(argv))
            code = run(argv, env=env, today=today)
            print(f"  (exit code {code})")


if __name__ == "__main__":  # pragma: no cover
    if len(sys.argv) > 1:  # `python -m … add yoga` behaves like the installed `habits` command
        sys.exit(run())
    main()  # no arguments: show the guided demo
