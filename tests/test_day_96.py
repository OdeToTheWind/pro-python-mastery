"""Tests for Day 96 – Packaging a Real Tool (scaffold built in tmp_path, no upload)."""

import importlib.util
import subprocess
import sys
import tomllib
import zipfile
from datetime import date

import pytest

from src.day_96_packaging_real_tool.main import (
    PUBLISH_WORKFLOW,
    VERSION,
    add_changelog_entry,
    bump_version,
    cli,
    main,
    plan_moves,
    preflight,
    render_core,
    render_pyproject,
    run_shipped_tests,
    scaffold,
    unique_destination,
    usage_markdown,
)


def make(folder, *names):
    for name in names:
        (folder / name).parent.mkdir(parents=True, exist_ok=True)
        (folder / name).write_text("x", encoding="utf-8")


def test_tool_sorts_files_without_overwriting(tmp_path, capsys):
    make(tmp_path, "a.JPG", "b.pdf", "documents/b.pdf", ".hidden.png", "notes", "images/old.png")
    assert cli([str(tmp_path)]) == 0
    assert sorted(p.relative_to(tmp_path).as_posix() for p in tmp_path.rglob("*") if p.is_file()) == [
        ".hidden.png", "documents/b (1).pdf", "documents/b.pdf", "images/a.JPG", "images/old.png", "other/notes"]
    assert "moved a.JPG -> images/a.JPG" in capsys.readouterr().out


def test_dry_run_and_errors(tmp_path, capsys):
    make(tmp_path, "song.mp3")
    assert cli(["-n", str(tmp_path)]) == 0 and (tmp_path / "song.mp3").exists()
    assert "would move song.mp3 -> audio/song.mp3" in capsys.readouterr().out
    assert cli([str(tmp_path / "missing")]) == 2 and "is not a folder" in capsys.readouterr().err
    empty = tmp_path / "empty"
    empty.mkdir()
    assert cli([str(empty)]) == 0 and capsys.readouterr().out.strip() == "nothing to tidy"


def test_unique_destination_and_planned_collisions(tmp_path):
    make(tmp_path, "r.pdf", "r (1).pdf")
    assert unique_destination(tmp_path / "r.pdf").name == "r (2).pdf"
    make(tmp_path / "in", "x.txt", "documents/x.txt")
    targets = [dest.name for _src, dest in plan_moves(tmp_path / "in")]
    assert targets == ["x (1).txt"]


def test_pyproject_is_complete():
    meta = tomllib.loads(render_pyproject())
    assert meta["project"]["scripts"] == {"tidyfiles": "tidyfiles.cli:main"}
    assert meta["project"]["dynamic"] == ["version"] and "Changelog" in meta["project"]["urls"]
    assert meta["tool"]["hatch"]["version"]["path"] == "src/tidyfiles/__init__.py"


def test_core_is_single_sourced():
    source = render_core()
    compile(source, "cli.py", "exec")
    assert "def main(argv" in source and "def cli(" not in source and "from . import __version__" in source


def test_usage_docs_come_from_the_parser():
    docs = usage_markdown()
    assert docs.startswith("## Usage") and "--dry-run" in docs and "tidyfiles [-h]" in docs


@pytest.mark.parametrize(("part", "expected"), [("major", "2.0.0"), ("minor", "1.5.0"), ("patch", "1.4.10")])
def test_bump_version(part, expected):
    assert bump_version("1.4.9", part) == expected


def test_bump_version_errors_and_changelog():
    with pytest.raises(ValueError, match="MAJOR.MINOR.PATCH"):
        bump_version("1.0", "patch")
    with pytest.raises(ValueError, match="part must"):
        bump_version("1.0.0", "huge")
    log = add_changelog_entry("# Changelog\n\n", "1.0.0", ["first"], date(2026, 1, 1))
    log = add_changelog_entry(log, "1.1.0", ["dry-run flag"], date(2026, 2, 1))
    assert log.index("## [1.1.0]") < log.index("## [1.0.0]")
    with pytest.raises(ValueError, match="already released"):
        add_changelog_entry(log, "1.0.0", ["again"], date(2026, 3, 1))


def test_preflight_green_then_catches_each_problem(tmp_path):
    project = scaffold(tmp_path)
    assert preflight(project) == []
    (project / "README.md").write_text("# tidyfiles\n\n## Usage\n\nold text\n")
    (project / "CHANGELOG.md").write_text("# Changelog\n")
    (project / "tests" / "test_cli.py").unlink()
    (project / ".github" / "workflows" / "publish.yml").write_text("on: push\n")
    assert preflight(project) == [
        f"changelog: no entry for {VERSION}", "docs: usage section is out of date – regenerate it",
        "tests: no tests shipped", "publish: TestPyPI trusted-publishing workflow missing"]
    (project / "src" / "tidyfiles" / "__init__.py").write_text('__version__ = "dev"\n')
    (project / "pyproject.toml").write_text('[project]\nname = "tidyfiles"\n')
    problems = preflight(project)
    assert "pyproject: missing project.scripts" in problems
    assert "version: __version__ missing or not MAJOR.MINOR.PATCH" in problems


def test_workflow_uses_trusted_publishing():
    assert "id-token: write" in PUBLISH_WORKFLOW and "password" not in PUBLISH_WORKFLOW
    assert "repository-url: https://test.pypi.org/legacy/" in PUBLISH_WORKFLOW


def test_shipped_tests_pass_against_generated_package(tmp_path):
    result = run_shipped_tests(scaffold(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr
    assert "2 passed" in result.stdout


@pytest.mark.skipif(not all(importlib.util.find_spec(m) for m in ("build", "hatchling")),
                    reason="install requirements-dev.txt (build, hatchling)")
def test_wheel_declares_entry_point_and_version(tmp_path):
    project = scaffold(tmp_path, version="1.2.3")
    subprocess.run([sys.executable, "-m", "build", "--wheel", "--no-isolation", "--outdir", str(tmp_path / "dist"),
                    str(project)], check=True, capture_output=True, timeout=300)
    (wheel,) = (tmp_path / "dist").glob("tidyfiles-1.2.3-*.whl")
    with zipfile.ZipFile(wheel) as zf:
        entry_points = zf.read("tidyfiles-1.2.3.dist-info/entry_points.txt").decode()
        metadata = zf.read("tidyfiles-1.2.3.dist-info/METADATA").decode()
        assert "tidyfiles/py.typed" in zf.namelist()
    assert "tidyfiles = tidyfiles.cli:main" in entry_points
    assert "Requires-Python: >=3.12" in metadata and "## Usage" in metadata


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "pre-flight: all green" in out and "license: LICENSE file missing" in out and "1.1.0" in out
