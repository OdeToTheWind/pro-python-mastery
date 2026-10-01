"""Study one day of the course in the terminal.

Usage::

    python scripts/learn.py            # asks for a day number
    python scripts/learn.py 18         # study Day 18
    python scripts/learn.py 18 --demo  # …and run its demo at the end
    python scripts/learn.py 18 --no-tests

For the chosen day it prints, in this order:

1. what the day is about (topic, level, phase, scenario),
2. what you will learn (syllabus deliverables) and **where each one lives in the code**,
3. the key learnings and pitfalls from the day's notes,
4. what the tests prove, then runs them so you see them pass,
5. ideas to experiment with, and the next step.

Everything comes from the repository itself – syllabus.md, the day's module, its tests and
``docs/progress/notes/day-XX.json`` – so it is always in step with the code.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import importlib
import importlib.util
import inspect
import json
import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import build_reflections as br  # noqa: E402

WIDTH = min(100, shutil.get_terminal_size((100, 20)).columns)


class Style:
    """ANSI colours only on a real terminal, and never when NO_COLOR is set."""

    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled

    def _wrap(self, code: str, text: str) -> str:
        return f"\033[{code}m{text}\033[0m" if self.enabled else text

    def title(self, text: str) -> str:
        return self._wrap("1;36", text)

    def heading(self, text: str) -> str:
        return self._wrap("1;33", text)

    def dim(self, text: str) -> str:
        return self._wrap("2", text)

    def code(self, text: str) -> str:
        return self._wrap("32", text)


def wrap(text: str, indent: str = "  ") -> str:
    """Wrap to the terminal width; continuation lines line up under the text, not the bullet."""
    return textwrap.fill(" ".join(text.split()), WIDTH, initial_indent=indent,
                         subsequent_indent=" " * len(indent))


def phase_of(day: int) -> str:
    for number, name, first, last in br.phases():
        if first <= day <= last:
            return f"Phase {number} · {name} (Days {first}–{last})"
    return "–"


def locate(module: Any, dotted: str) -> tuple[str, str]:
    """``(where, summary)`` for a DELIVERABLES target: file:line plus signature or value."""
    target = module
    for part in dotted.split("."):
        target = getattr(target, part)
    try:
        lines, start = inspect.getsourcelines(target)
        source_file = Path(inspect.getsourcefile(target) or "")
        where = f"{source_file.relative_to(ROOT).as_posix()}:{start}"
    except (TypeError, OSError, ValueError):
        where = f"{Path(module.__file__).relative_to(ROOT).as_posix()} (constant)"
    if inspect.isclass(target) or inspect.isfunction(target) or inspect.ismethod(target):
        doc = (inspect.getdoc(target) or "").split("\n\n")[0]
        try:
            signature = f"{dotted}{inspect.signature(target)}".replace("'", "")
        except (TypeError, ValueError):
            signature = dotted
        return where, signature + (f" — {' '.join(doc.split())}" if doc else "")
    text = repr(target)
    return where, f"{dotted} = {text if len(text) <= 70 else text[:67] + '...'}"


def test_names(day: int) -> list[str]:
    tree = ast.parse((ROOT / "tests" / f"test_day_{day:02d}.py").read_text(encoding="utf-8"))
    return [node.name for node in tree.body if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")]


def explain(day: int, style: Style) -> None:
    rows = br.syllabus_rows()
    row = rows[day]
    folder = br.day_dir(day)
    module = importlib.import_module(f"src.{folder.name}.main")
    notes = json.loads((ROOT / "docs" / "progress" / "notes" / f"day-{day:02d}.json").read_text(encoding="utf-8"))
    rule = "─" * WIDTH

    print(style.title(rule))
    print(style.title(f"  Day {day} · {row['topic']}"))
    print(style.dim(f"  {row['level']} · {phase_of(day)}"))
    print(style.title(rule))

    print(style.heading("\n▸ The scenario"))
    print(wrap(br.scenario(module.__doc__ or "")))

    print(style.heading("\n▸ What you will learn"))
    print(wrap(row["deliverables"]))

    print(style.heading("\n▸ Where each skill lives in the code"))
    for skill, target in module.DELIVERABLES.items():
        where, summary = locate(module, target)
        print(f"  • {skill}")
        print(f"      {style.code(where)}")
        print(textwrap.fill(summary, WIDTH, initial_indent="      ", subsequent_indent="        "))

    print(style.heading("\n▸ Key learnings"))
    for item in notes["learnings"]:
        print(wrap(item, "  • "))
    print(style.heading("\n▸ Pitfalls to avoid"))
    for item in notes["pitfalls"]:
        print(wrap(item, "  ⚠ "))

    names = test_names(day)
    print(style.heading(f"\n▸ What the {len(names)} tests prove"))
    for name in names:
        print(f"  ✓ {name.removeprefix('test_').replace('_', ' ')}")


def run_tests(day: int, style: Style) -> int:
    print(style.heading(f"\n▸ Running tests/test_day_{day:02d}.py"))
    command = [sys.executable, "-m", "pytest", f"tests/test_day_{day:02d}.py", "-v", "--no-header",
               "-p", "no:cacheprovider", "--no-cov"]
    if importlib.util.find_spec("pytest_cov") is None:
        command.remove("--no-cov")
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def run_demo(day: int, style: Style) -> int:
    folder = br.day_dir(day)
    print(style.heading(f"\n▸ Demo: python -m src.{folder.name}.main"))
    return subprocess.run([sys.executable, "-m", f"src.{folder.name}.main"], cwd=ROOT, check=False).returncode


def next_steps(day: int, style: Style) -> None:
    folder = br.day_dir(day)
    notes = json.loads((ROOT / "docs" / "progress" / "notes" / f"day-{day:02d}.json").read_text(encoding="utf-8"))
    print(style.heading("\n▸ Try it yourself"))
    print(f"  1. Open {style.code(f'src/{folder.name}/main.py')} and change one line of a function listed above.")
    print(f"  2. Re-run {style.code(f'./propython.sh {day}')} – watch a test turn red and read why.")
    print("  3. Undo the change (or fix it properly) until everything is green again.")
    print(f"  4. Read the full reflection: {style.code(f'docs/progress/day-{day:02d}-reflection.md')}")
    print(style.heading("\n▸ Next step"))
    print(wrap(notes["next"]))
    print()


def ask_day(prompt: str = "Which day do you want to study? (1–100, q to quit): ") -> int | None:
    while True:
        try:
            answer = input(prompt).strip().lower()
        except EOFError:
            return None
        if answer in {"q", "quit", "exit", ""}:
            return None
        if answer.isdigit() and 1 <= int(answer) <= 100:
            return int(answer)
        print("  Please enter a whole number from 1 to 100.")


def ask_yes(prompt: str) -> bool:
    try:
        return input(prompt).strip().lower() in {"y", "yes"}
    except EOFError:
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="learn", description="Study one day: explanation, code map and tests.")
    parser.add_argument("day", nargs="?", type=int, help="day number 1–100 (asked for when omitted)")
    parser.add_argument("--demo", action="store_true", help="run the day's demo without asking")
    parser.add_argument("--no-tests", action="store_true", help="explain only, do not run the tests")
    args = parser.parse_args(argv)

    with contextlib.suppress(AttributeError, ValueError):  # emoji on Windows consoles
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    interactive = sys.stdin.isatty()
    style = Style(sys.stdout.isatty() and "NO_COLOR" not in os.environ)

    day = args.day if args.day is not None else ask_day()
    if day is None:
        return 0
    if day not in br.syllabus_rows():
        print(f"There is no Day {day}. Choose a number from 1 to 100.", file=sys.stderr)
        return 2
    if br.syllabus_rows()[day]["status"] != "Covered":
        print(f"Day {day} is planned but not written yet.", file=sys.stderr)
        return 2

    explain(day, style)
    code = 0 if args.no_tests else run_tests(day, style)
    if args.demo or (interactive and ask_yes("\nRun the demo now? [y/N] ")):
        run_demo(day, style)
    next_steps(day, style)
    return code


if __name__ == "__main__":
    sys.exit(main())
