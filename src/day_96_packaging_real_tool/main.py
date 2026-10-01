"""Day 96 – Capstone: Packaging a Real Tool.

Scenario: ship ``tidyfiles`` – a *downloads-folder organiser* that sorts
files into ``images/``, ``documents/``, ``archives/`` … – as a release-ready
project. Day 79 learned the packaging mechanics; today is the **release
engineering** around a working tool: the tool's code is single-sourced into
the package, usage docs are generated from the real ``argparse`` parser, the
project ships its own tests, versions are bumped with a changelog, a
pre-flight check blocks incomplete releases, and a GitHub Actions workflow
publishes to TestPyPI with trusted publishing (no API token stored).

Deliverables (syllabus):
* A complete ``pyproject.toml`` (metadata, classifiers, URLs, scripts,
  dynamic version, pytest/coverage config)
* A CLI entry point (``tidyfiles = "tidyfiles.cli:main"``)
* Documentation (README + usage generated from the parser, CHANGELOG)
* Tests shipped with the project and run against the generated package
* TestPyPI publishing (trusted-publishing workflow, release pre-flight)
"""

from __future__ import annotations

import argparse
import inspect
import os
import re
import shutil
import subprocess
import sys
import tomllib
from datetime import date
from pathlib import Path

DELIVERABLES: dict[str, str] = {
    "the real tool: plan and apply moves": "plan_moves",
    "CLI entry point": "cli",
    "complete pyproject.toml": "render_pyproject",
    "docs generated from the parser": "usage_markdown",
    "semantic version bump + changelog": "bump_version",
    "project scaffold with shipped tests": "scaffold",
    "release pre-flight checks": "preflight",
    "TestPyPI trusted-publishing workflow": "PUBLISH_WORKFLOW",
}

VERSION = "1.0.0"
CATEGORIES: dict[str, set[str]] = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp"},
    "documents": {".pdf", ".docx", ".txt", ".md", ".odt"},
    "archives": {".zip", ".tar", ".gz", ".7z"},
    "audio": {".mp3", ".wav", ".flac"},
}


# --- the tool itself (copied verbatim into the package by ``scaffold``) -------
def categorise(path: Path) -> str:
    suffix = path.suffix.lower()
    return next((name for name, suffixes in CATEGORIES.items() if suffix in suffixes), "other")


def unique_destination(dest: Path) -> Path:
    """Never overwrite: report.pdf → report (1).pdf → report (2).pdf …"""
    candidate, n = dest, 1
    while candidate.exists():
        candidate = dest.with_name(f"{dest.stem} ({n}){dest.suffix}")
        n += 1
    return candidate


def plan_moves(folder: Path) -> list[tuple[Path, Path]]:
    """Top-level, non-hidden files only; already-sorted folders are left alone."""
    moves: list[tuple[Path, Path]] = []
    claimed: set[Path] = set()
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.name.startswith("."):
            continue
        dest = unique_destination(folder / categorise(path) / path.name)
        while dest in claimed:  # two planned moves must not collide either
            dest = unique_destination(dest.with_name(f"{dest.stem}_{len(claimed)}{dest.suffix}"))
        claimed.add(dest)
        moves.append((path, dest))
    return moves


def apply_moves(moves: list[tuple[Path, Path]], dry_run: bool = False) -> list[str]:
    report = []
    for src, dest in moves:
        report.append(f"{'would move' if dry_run else 'moved'} {src.name} -> {dest.parent.name}/{dest.name}")
        if not dry_run:
            dest.parent.mkdir(exist_ok=True)
            src.rename(dest)
    return report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tidyfiles", description="Sort a messy folder into category folders.")
    parser.add_argument("folder", type=Path, help="folder to tidy (e.g. ~/Downloads)")
    parser.add_argument("-n", "--dry-run", action="store_true", help="show what would move, change nothing")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    return parser


def cli(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    folder = args.folder.expanduser()
    if not folder.is_dir():
        print(f"tidyfiles: {folder} is not a folder", file=sys.stderr)
        return 2
    lines = apply_moves(plan_moves(folder), dry_run=args.dry_run)
    print("\n".join(lines) or "nothing to tidy")
    return 0


TOOL_OBJECTS = (categorise, unique_destination, plan_moves, apply_moves, build_parser, cli)


# --- release engineering -----------------------------------------------------------
def render_core() -> str:
    """Single source of truth: the package's code *is* the code tested above."""
    header = (
        '"""tidyfiles – sort a messy folder into category folders."""\n\n'
        "from __future__ import annotations\n\nimport argparse\nimport sys\nfrom pathlib import Path\n\n"
        "from . import __version__ as VERSION\n\n"
        f"CATEGORIES: dict[str, set[str]] = {CATEGORIES!r}\n\n\n"
    )
    body = "\n\n".join(inspect.getsource(obj) for obj in TOOL_OBJECTS)
    return header + body.replace("def cli(", "def main(")


def render_pyproject(version_file: str = "src/tidyfiles/__init__.py") -> str:
    return f'''[build-system]
requires = ["hatchling>=1.25"]
build-backend = "hatchling.build"

[project]
name = "tidyfiles"
dynamic = ["version"]
description = "Sort a messy downloads folder into tidy category folders."
readme = "README.md"
requires-python = ">=3.12"
license = "MIT"
authors = [{{ name = "Pro Python Mastery", email = "maintainers@example.org" }}]
keywords = ["files", "cli", "organiser"]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Topic :: Utilities",
]
dependencies = []

[project.optional-dependencies]
test = ["pytest>=8", "pytest-cov>=5"]

[project.scripts]
tidyfiles = "tidyfiles.cli:main"

[project.urls]
Homepage = "https://github.com/OdeToTheWind/pro-python-mastery"
Changelog = "https://github.com/OdeToTheWind/pro-python-mastery/blob/main/CHANGELOG.md"
Issues = "https://github.com/OdeToTheWind/pro-python-mastery/issues"

[tool.hatch.version]
path = "{version_file}"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"

[tool.coverage.report]
fail_under = 90
'''


def usage_markdown() -> str:
    """Docs generated from the real parser can never drift from the code."""
    help_text = build_parser().format_help().replace("usage: ", "", 1)
    return f"## Usage\n\n```text\n$ tidyfiles --help\n{help_text}```\n"


SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def bump_version(version: str, part: str) -> str:
    match = SEMVER.match(version)
    if not match:
        raise ValueError(f"not a MAJOR.MINOR.PATCH version: {version!r}")
    major, minor, patch = map(int, match.groups())
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    if part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError("part must be major, minor or patch")


def add_changelog_entry(changelog: str, version: str, changes: list[str], on: date) -> str:
    if f"## [{version}]" in changelog:
        raise ValueError(f"version {version} already released")
    entry = f"## [{version}] – {on.isoformat()}\n\n" + "".join(f"- {c}\n" for c in changes) + "\n"
    head, sep, rest = changelog.partition("## [")
    return head + entry + (sep + rest if sep else "")


PUBLISH_WORKFLOW = """name: publish-testpypi
on:
  push:
    tags: ["v*"]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: "3.12"}
      - run: python -m pip install build twine && python -m build && python -m twine check dist/*
      - uses: actions/upload-artifact@v4
        with: {name: dist, path: dist/}
  publish:
    needs: build
    runs-on: ubuntu-latest
    environment: testpypi
    permissions:
      id-token: write  # trusted publishing: GitHub proves who we are, no API token is stored
    steps:
      - uses: actions/download-artifact@v4
        with: {name: dist, path: dist/}
      - uses: pypa/gh-action-pypi-publish@release/v1
        with:
          repository-url: https://test.pypi.org/legacy/
"""

TEST_FILE = '''from tidyfiles.cli import main, plan_moves


def test_sorts_and_never_overwrites(tmp_path):
    for name in ("a.jpg", "b.pdf", "c.xyz"):
        (tmp_path / name).write_text("x")
    (tmp_path / "documents").mkdir()
    (tmp_path / "documents" / "b.pdf").write_text("old")
    assert main([str(tmp_path)]) == 0
    assert (tmp_path / "images" / "a.jpg").exists()
    assert (tmp_path / "documents" / "b (1).pdf").exists()
    assert (tmp_path / "other" / "c.xyz").exists()


def test_dry_run_changes_nothing(tmp_path):
    (tmp_path / "song.mp3").write_text("x")
    assert main(["--dry-run", str(tmp_path)]) == 0
    assert plan_moves(tmp_path)[0][1].parent.name == "audio"
'''


def scaffold(root: Path, version: str = VERSION, changes: tuple[str, ...] = ("First public release",)) -> Path:
    project = root / "tidyfiles"
    package = project / "src" / "tidyfiles"
    package.mkdir(parents=True, exist_ok=True)
    (project / "tests").mkdir(exist_ok=True)
    (project / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
    files = {
        project / "pyproject.toml": render_pyproject(),
        package / "__init__.py": f'"""tidyfiles – folder organiser."""\n\n__version__ = "{version}"\n',
        package / "cli.py": render_core(),
        package / "__main__.py": "from .cli import main\n\nraise SystemExit(main())\n",
        package / "py.typed": "",
        project / "tests" / "test_cli.py": TEST_FILE,
        project / "README.md": "# tidyfiles\n\nSort a messy downloads folder into tidy category folders.\n\n"
                               "```bash\npip install tidyfiles\n```\n\n" + usage_markdown(),
        project / "CHANGELOG.md": add_changelog_entry("# Changelog\n\n", version, list(changes), date(2026, 10, 1)),
        project / "LICENSE": "MIT License\n\nCopyright (c) 2026 Pro Python Mastery\n",
        project / ".github" / "workflows" / "publish.yml": PUBLISH_WORKFLOW,
    }
    for path, content in files.items():
        path.write_text(content, encoding="utf-8")
    return project


def preflight(project: Path) -> list[str]:
    """Everything a maintainer forgets at 23:00 on release night."""
    problems = []
    meta = tomllib.loads((project / "pyproject.toml").read_text(encoding="utf-8"))
    proj = meta.get("project", {})
    for key in ("description", "readme", "requires-python", "license", "authors", "classifiers", "urls", "scripts"):
        if not proj.get(key):
            problems.append(f"pyproject: missing project.{key}")
    init = project / "src" / "tidyfiles" / "__init__.py"
    found = re.search(r'__version__ = "([^"]+)"', init.read_text(encoding="utf-8")) if init.exists() else None
    version = found.group(1) if found else None
    if version is None or not SEMVER.match(version):
        problems.append("version: __version__ missing or not MAJOR.MINOR.PATCH")
    changelog = project / "CHANGELOG.md"
    if not changelog.exists() or f"## [{version}]" not in changelog.read_text(encoding="utf-8"):
        problems.append(f"changelog: no entry for {version}")
    readme = project / "README.md"
    if not readme.exists() or "## Usage" not in readme.read_text(encoding="utf-8"):
        problems.append("docs: README has no usage section")
    elif usage_markdown() not in readme.read_text(encoding="utf-8"):
        problems.append("docs: usage section is out of date – regenerate it")
    if not list((project / "tests").glob("test_*.py")):
        problems.append("tests: no tests shipped")
    if not (project / "LICENSE").exists():
        problems.append("license: LICENSE file missing")
    workflow = project / ".github" / "workflows" / "publish.yml"
    text = workflow.read_text(encoding="utf-8") if workflow.exists() else ""
    if "id-token: write" not in text or "test.pypi.org" not in text:
        problems.append("publish: TestPyPI trusted-publishing workflow missing")
    return problems


def run_shipped_tests(project: Path) -> subprocess.CompletedProcess[str]:
    """Run the project's own tests against its ``src`` package, exactly as CI would."""
    return subprocess.run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "tests"],
                          cwd=project, capture_output=True, text=True, timeout=120, check=False,
                          env={**os.environ, "PYTHONPATH": str(project / "src")})


def main() -> None:
    import tempfile

    print("Day 96 – Releasing tidyfiles\n")
    with tempfile.TemporaryDirectory() as tmp:
        downloads = Path(tmp) / "Downloads"
        downloads.mkdir()
        for name in ("holiday.jpg", "invoice.pdf", "invoice (copy).pdf", "backup.zip", "mystery.bin"):
            (downloads / name).write_text("x", encoding="utf-8")
        cli([str(downloads), "--dry-run"])
        project = scaffold(Path(tmp))
        print("\npre-flight:", preflight(project) or "all green")
        (project / "LICENSE").unlink()
        print("after deleting LICENSE:", preflight(project))
        print("next version:", bump_version(VERSION, "minor"))
        if shutil.which("git") is None:  # pragma: no cover
            print("(git not installed – tag manually)")
        print("release: git tag v1.0.0 && git push --tags  → workflow publishes to TestPyPI")


if __name__ == "__main__":
    main()
