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
./propython.sh {day}                 # study mode: explanation, code map, notes and tests
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


PHASE = re.compile(r"^## Phase (\d+) · (.+?) \(Days (\d+)–(\d+)\)$")


def phases() -> list[tuple[int, str, int, int]]:
    """``(number, name, first_day, last_day)`` from the ``## Phase …`` headings in syllabus.md."""
    found = []
    for line in (ROOT / "syllabus.md").read_text(encoding="utf-8").splitlines():
        if match := PHASE.match(line):
            number, name, first, last = match.groups()
            found.append((int(number), name, int(first), int(last)))
    return found


def phase_status(rows: dict[int, dict[str, str]]) -> str:
    """Three-column progress table: one line per phase."""
    lines = ["| Phase | Days | Status |", "|---|:-:|---|"]
    for number, name, first, last in phases():
        total = last - first + 1
        done = sum(rows[d]["status"] == "Covered" for d in range(first, last + 1) if d in rows)
        state = "✅ Complete" if done == total else ("🟡 In progress" if done else "⬜ Planned")
        lines.append(f"| {number} · {name} | {first}–{last} | {state} ({done}/{total}) |")
    return "\n".join(lines)


def kpis(rows: dict[int, dict[str, str]]) -> str:
    """Numbers measured from the repository itself, so the README can never overstate them."""
    covered = [d for d, r in rows.items() if r["status"] == "Covered"]
    tests = sum(count_tests(d) for d in covered)
    source_lines = sum(len([ln for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()])
                       for f in (ROOT / "src").rglob("*.py"))
    deliverables = sum(len(importlib.import_module(f"src.{day_dir(d).name}.main").DELIVERABLES) for d in covered)
    workflow = (ROOT / ".github" / "workflows" / "python-tests.yml").read_text(encoding="utf-8")
    versions = re.search(r'python-version: \[(.+?)\]', workflow)
    gate = re.search(r"--cov-fail-under=(\d+)", workflow)
    systems = sorted({m for m in re.findall(r"(ubuntu|windows|macos)-latest", workflow)})
    return "\n".join([
        f"- **Curriculum completion:** {len(covered)} / {len(rows)} days covered, each with code, tests and a reflection.",
        f"- **Test functions:** {tests} across {len(covered)} test modules (parametrised cases run more).",
        f"- **Deliverables mapped to code:** {deliverables} `DELIVERABLES` entries, each checked to resolve.",
        f"- **Source size:** {source_lines:,} non-blank lines of Python in `src/`.",
        f"- **Coverage gate:** CI fails below {gate.group(1) if gate else '?'} % coverage (lines and branches).",
        f"- **Python versions in CI:** {versions.group(1).replace(chr(34), '') if versions else '?'}.",
        f"- **Operating systems in CI:** {', '.join(OS_NAMES[s] for s in systems)}.",
        "- **Quality checks per commit:** ruff lint · mypy type-check · pytest with coverage · syllabus sync.",
    ])


OS_NAMES = {"ubuntu": "Linux", "windows": "Windows", "macos": "macOS"}

README_BLOCKS = {
    "course-index": course_index,
    "phase-status": phase_status,
    "kpis": kpis,
}


def render_readme(text: str, rows: dict[int, dict[str, str]]) -> str:
    for name, build in README_BLOCKS.items():
        start, end = f"<!-- {name}:start -->", f"<!-- {name}:end -->"
        if start not in text:
            continue
        before, rest = text.split(start, 1)
        _, after = rest.split(end, 1)
        text = f"{before}{start}\n{build(rows)}\n{end}{after}"
    return text


def update_readme(rows: dict[int, dict[str, str]]) -> None:
    readme = ROOT / "README.md"
    readme.write_text(render_readme(readme.read_text(encoding="utf-8"), rows), encoding="utf-8", newline="\n")


def main() -> None:
    rows = syllabus_rows()
    notes_dir = ROOT / "docs" / "progress" / "notes"
    written = 0
    for day, row in sorted(rows.items()):
        if row["status"] != "Covered":
            continue
        notes = json.loads((notes_dir / f"day-{day:02d}.json").read_text(encoding="utf-8"))
        target = ROOT / "docs" / "progress" / f"day-{day:02d}-reflection.md"
        target.write_text(render(day, row, notes, notes["date"]), encoding="utf-8", newline="\n")
        written += 1
    update_readme(rows)
    print(f"wrote {written} reflections and refreshed the README course index")


if __name__ == "__main__":
    main()
