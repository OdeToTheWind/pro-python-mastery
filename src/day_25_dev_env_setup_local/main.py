"""Day 25 – Local Development Environment Setup.

Scenario: a *project doctor* that inspects a checkout (this repository by
default) and reports whether the local environment follows best practice.

Deliverables (syllabus):
* Virtual environments (detect correctly, explain creation)
* Project structure
* Local development best practices (pinned deps, ignored secrets, tooling config)
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

DELIVERABLES: dict[str, str] = {
    "virtual environment detection": "in_virtualenv",
    "interpreter version check": "python_version_ok",
    "project structure check": "check_structure",
    "dependency hygiene": "audit_requirements",
    ".gitignore best practices": "missing_ignore_rules",
}

REQUIRED_PATHS = ("src", "tests", "pyproject.toml", "requirements.txt", ".gitignore", "README.md")
IGNORE_RULES = (".venv/", "__pycache__/", ".env")
MIN_PYTHON = (3, 12)
VENV_STEPS = (
    "python -m venv .venv",
    "source .venv/bin/activate      # Windows: .venv\\Scripts\\activate",
    "pip install -r requirements-dev.txt",
)


def in_virtualenv() -> bool:
    """True inside a venv – works even when ``activate`` was never run.

    A venv's interpreter sets ``sys.prefix`` to the venv folder while
    ``sys.base_prefix`` still points at the base installation. Checking the
    ``VIRTUAL_ENV`` variable instead misses IDE- and CI-launched interpreters.
    """
    return sys.prefix != sys.base_prefix


def python_version_ok(version: tuple[int, ...] = tuple(sys.version_info[:2])) -> bool:
    return version >= MIN_PYTHON


def check_structure(root: Path) -> dict[str, bool]:
    return {name: (root / name).exists() for name in REQUIRED_PATHS}


@dataclass(frozen=True, slots=True)
class RequirementsAudit:
    packages: list[str]
    duplicates: list[str]
    unpinned: list[str]


def audit_requirements(text: str) -> RequirementsAudit:
    """Find duplicate and unpinned packages in a requirements file."""
    names: list[str] = []
    duplicates: list[str] = []
    unpinned: list[str] = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or line.startswith("-"):
            continue
        match = re.match(r"([A-Za-z0-9_.\-\[\]]+)\s*(.*)", line)
        if not match:
            continue
        name = match.group(1).lower()
        if name in names:
            duplicates.append(name)
        else:
            names.append(name)
        if not match.group(2):
            unpinned.append(name)
    return RequirementsAudit(names, duplicates, unpinned)


def missing_ignore_rules(gitignore_text: str) -> list[str]:
    present = {line.strip() for line in gitignore_text.splitlines()}
    return [rule for rule in IGNORE_RULES if rule not in present]


def diagnose(root: Path) -> list[str]:
    report = [
        f"{'✅' if python_version_ok() else '❌'} Python {sys.version.split()[0]} (need ≥ 3.12)",
        f"{'✅' if in_virtualenv() else '⚠️ '} virtual environment {'active' if in_virtualenv() else 'not active'}",
    ]
    for name, exists in check_structure(root).items():
        report.append(f"{'✅' if exists else '❌'} {name}")
    req = root / "requirements.txt"
    if req.exists():
        audit = audit_requirements(req.read_text(encoding="utf-8"))
        report.append(f"   duplicates: {audit.duplicates or 'none'}; unpinned: {audit.unpinned or 'none'}")
    ignore = root / ".gitignore"
    if ignore.exists():
        report.append(f"   .gitignore missing: {missing_ignore_rules(ignore.read_text(encoding='utf-8')) or 'nothing'}")
    return report


def main(root: Path | None = None) -> None:
    root = root or Path(__file__).resolve().parents[2]
    print("Day 25 – Project doctor\n")
    print("\n".join(diagnose(root)))
    print("\nCreate a fresh environment:")
    for step in VENV_STEPS:
        print("  $", step)


if __name__ == "__main__":
    main()
