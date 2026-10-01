"""Keep syllabus.md, src/, tests/ and docs/progress/ in lock-step.

A day may only be marked **Covered** when its code, tests and reflection all
exist and agree. A **Planned** day must not have code yet (otherwise the
status is understated). Reflections must equal what
``scripts/build_reflections.py`` would generate right now.
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_reflections  # noqa: E402

ROWS = build_reflections.syllabus_rows()
COVERED = sorted(day for day, row in ROWS.items() if row["status"] == "Covered")
PLANNED = sorted(day for day, row in ROWS.items() if row["status"] == "Planned")


def resolve(module: object, dotted: str) -> object:
    target = module
    for part in dotted.split("."):
        target = getattr(target, part)
    return target


def test_syllabus_has_100_unique_days_with_known_statuses():
    assert sorted(ROWS) == list(range(1, 101))
    assert {row["status"] for row in ROWS.values()} <= {"Covered", "Planned"}
    assert list(range(1, len(COVERED) + 1)) == COVERED, "days must be covered in order"


@pytest.mark.parametrize("day", COVERED)
def test_covered_day_has_code_with_resolvable_deliverables(day):
    folders = list((ROOT / "src").glob(f"day_{day:02d}_*"))
    assert len(folders) == 1, f"expected exactly one src folder for day {day}"
    module = importlib.import_module(f"src.{folders[0].name}.main")
    assert "Scenario:" in (module.__doc__ or ""), "module docstring must describe the scenario"
    deliverables = getattr(module, "DELIVERABLES", None)
    assert isinstance(deliverables, dict) and len(deliverables) >= 2
    for name, target in deliverables.items():
        assert resolve(module, target) is not None, f"{name!r} points to missing {target!r}"
    assert callable(getattr(module, "main", None)), "every day needs a runnable main()"


@pytest.mark.parametrize("day", COVERED)
def test_covered_day_tests_exercise_src(day):
    (folder,) = (ROOT / "src").glob(f"day_{day:02d}_*")
    source = (ROOT / "tests" / f"test_day_{day:02d}.py").read_text(encoding="utf-8")
    assert f"src.{folder.name}" in source, "tests must import the day's own code"
    assert build_reflections.count_tests(day) >= 5, "each day needs a meaningful set of tests"
    assert "assert True" not in source, "placeholder assertions are not allowed"


@pytest.mark.parametrize("day", COVERED)
def test_reflection_is_generated_from_current_code(day):
    notes = json.loads((ROOT / "docs" / "progress" / "notes" / f"day-{day:02d}.json").read_text(encoding="utf-8"))
    assert notes["learnings"] and notes["pitfalls"] and notes["next"]
    expected = build_reflections.render(day, ROWS[day], notes, notes["date"])
    actual = (ROOT / "docs" / "progress" / f"day-{day:02d}-reflection.md").read_text(encoding="utf-8")
    assert actual == expected, "reflection is stale – run: python scripts/build_reflections.py"


@pytest.mark.parametrize("day", PLANNED)
def test_planned_day_has_no_code_yet(day):
    assert not list((ROOT / "src").glob(f"day_{day:02d}_*")), (
        f"day {day} has code – mark it Covered in syllabus.md (with tests and a reflection)")
    assert not (ROOT / "tests" / f"test_day_{day:02d}.py").exists()


def test_scenarios_are_unique_per_day():
    scenarios = {}
    for day in COVERED:
        (folder,) = (ROOT / "src").glob(f"day_{day:02d}_*")
        doc = importlib.import_module(f"src.{folder.name}.main").__doc__ or ""
        scenarios[day] = build_reflections.scenario(doc)
    duplicates = {s for s in scenarios.values() if list(scenarios.values()).count(s) > 1}
    assert not duplicates, f"each day needs its own scenario: {duplicates}"


def test_readme_generated_blocks_are_current():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for name in build_reflections.README_BLOCKS:
        assert f"<!-- {name}:start -->" in readme, f"README lost its generated {name!r} block"
    assert readme == build_reflections.render_readme(readme, ROWS), (
        "README generated blocks are stale – run: python scripts/build_reflections.py")


def test_syllabus_phases_cover_every_day_once():
    days = [d for _n, _name, first, last in build_reflections.phases() for d in range(first, last + 1)]
    assert days == list(range(1, 101)), "phase headings in syllabus.md must cover days 1–100 in order"
