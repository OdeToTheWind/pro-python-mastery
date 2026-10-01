"""Regenerate every Covered day's reflection from the source of truth.

Usage: ``python scripts/build_reflections.py``

For each Covered day it reads:
* the syllabus row (topic, deliverables, level),
* the day module's docstring scenario and ``DELIVERABLES`` map,
* the number of tests in ``tests/test_day_XX.py``,
* hand-written notes from ``docs/progress/notes/day-XX.json`` (learnings, pitfalls, next step),
and writes ``docs/progress/day-XX-reflection.md``. ``tests/test_syllabus_sync.py``
checks that the files stay consistent with the code.
"""

from __future__ import annotations

import ast
import importlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(\w+)\s*\|\s*(\w+)\s*\|$")


def syllabus_rows() -> dict[int, dict[str, str]]:
    rows = {}
    for line in (ROOT / "syllabus.md").read_text(encoding="utf-8").splitlines():
        if match := ROW.match(line):
            day, topic, deliverables, level, status = match.groups()
            rows[int(day)] = {"topic": topic, "deliverables": deliverables, "level": level, "status": status}
    return rows


def day_dir(day: int) -> Path:
    (path,) = (ROOT / "src").glob(f"day_{day:02d}_*")
    return path


def scenario(module_doc: str) -> str:
    match = re.search(r"Scenario:\s*(.+?)(?:\n\n|$)", module_doc, re.S)
    text = " ".join(match.group(1).split()) if match else ""
    return text[:1].upper() + text[1:]


def count_tests(day: int) -> int:
    tree = ast.parse((ROOT / "tests" / f"test_day_{day:02d}.py").read_text(encoding="utf-8"))
    return sum(isinstance(n, ast.FunctionDef) and n.name.startswith("test_") for n in tree.body)


def _escape(text: str) -> str:
    """Stop Markdown from turning ``*args`` or ``__init__`` into emphasis."""
    return text.replace("\\", "\\\\").replace("*", "\\*").replace("_", "\\_")


def render(day: int, row: dict[str, str], notes: dict[str, object], date: str) -> str:
    folder = day_dir(day)
    module = importlib.import_module(f"src.{folder.name}.main")
    deliverables: dict[str, str] = module.DELIVERABLES
    table = "\n".join(f"| ✅ {_escape(name)} | `{target}` |" for name, target in deliverables.items())
    learnings = "\n".join(f"- {item}" for item in notes["learnings"])  # type: ignore[union-attr]
    pitfalls = "\n".join(f"- {item}" for item in notes["pitfalls"])  # type: ignore[union-attr]
    return f"""# Day {day:02d} – {row['topic']} Reflection

**Date:** {date} · **Level:** {row['level']} · **Python:** 3.12+ · **Status:** {row['status']}
**Code:** [`src/{folder.name}/main.py`](../../src/{folder.name}/main.py) · **Tests:** [`tests/test_day_{day:02d}.py`](../../tests/test_day_{day:02d}.py) ({count_tests(day)} tests)

## Scenario
{scenario(module.__doc__ or '')}

## Syllabus deliverables
> {_escape(row['deliverables'])}

| Deliverable | Implemented in |
|---|---|
{table}

## Key learnings
{learnings}

## Pitfalls I hit (and how I fixed them)
{pitfalls}

## Run it
```bash
python -m src.{folder.name}.main
pytest tests/test_day_{day:02d}.py -v
```

## Next step
- {notes['next']}
"""


INDEX_START, INDEX_END = "<!-- course-index:start -->", "<!-- course-index:end -->"
LEVEL_BADGE = {"Beginner": "🟢", "Intermediate": "🟡", "Advanced": "🟠", "Capstone": "🔴"}


def course_index(rows: dict[int, dict[str, str]]) -> str:
    """Markdown table for the README: one line per day, linking code, tests and reflection."""
    lines = ["| Day | Topic | Level | Scenario you build | Links |", "|---:|---|:-:|---|---|"]
    for day, row in sorted(rows.items()):
        badge = LEVEL_BADGE.get(row["level"], "")
        if row["status"] != "Covered":
            lines.append(f"| {day} | {row['topic']} | {badge} | _planned_ | – |")
            continue
        folder = day_dir(day)
        module = importlib.import_module(f"src.{folder.name}.main")
        links = (f"[code](src/{folder.name}/main.py) · [tests](tests/test_day_{day:02d}.py) · "
                 f"[notes](docs/progress/day-{day:02d}-reflection.md)")
        lines.append(f"| {day} | {row['topic']} | {badge} | {scenario(module.__doc__ or '')} | {links} |")
    return "\n".join(lines)


def update_readme(rows: dict[int, dict[str, str]]) -> None:
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    before, rest = text.split(INDEX_START, 1)
    _, after = rest.split(INDEX_END, 1)
    readme.write_text(f"{before}{INDEX_START}\n{course_index(rows)}\n{INDEX_END}{after}", encoding="utf-8")


def main() -> None:
    rows = syllabus_rows()
    notes_dir = ROOT / "docs" / "progress" / "notes"
    written = 0
    for day, row in sorted(rows.items()):
        if row["status"] != "Covered":
            continue
        notes = json.loads((notes_dir / f"day-{day:02d}.json").read_text(encoding="utf-8"))
        target = ROOT / "docs" / "progress" / f"day-{day:02d}-reflection.md"
        target.write_text(render(day, row, notes, notes["date"]), encoding="utf-8")
        written += 1
    update_readme(rows)
    print(f"wrote {written} reflections and refreshed the README course index")


if __name__ == "__main__":
    main()
