"""Tests for Day 25 – Local Development Environment Setup."""

import sys
from pathlib import Path

from src.day_25_dev_env_setup_local.main import (
    REQUIRED_PATHS,
    audit_requirements,
    check_structure,
    diagnose,
    in_virtualenv,
    main,
    missing_ignore_rules,
    python_version_ok,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_in_virtualenv_matches_prefixes(monkeypatch):
    monkeypatch.setattr(sys, "prefix", "/project/.venv")
    monkeypatch.setattr(sys, "base_prefix", "/usr")
    assert in_virtualenv() is True
    monkeypatch.setattr(sys, "prefix", "/usr")
    assert in_virtualenv() is False


def test_python_version_ok():
    assert python_version_ok((3, 12)) and python_version_ok((3, 14))
    assert not python_version_ok((3, 9))


def test_this_repository_has_the_recommended_structure():
    assert all(check_structure(REPO_ROOT).values())


def test_check_structure_on_empty_dir(tmp_path):
    (tmp_path / "src").mkdir()
    result = check_structure(tmp_path)
    assert result["src"] is True
    assert [name for name, ok in result.items() if not ok] == list(REQUIRED_PATHS[1:])


def test_audit_requirements():
    audit = audit_requirements("pytest\npytest\nrequests>=2.31  # http\n-r base.txt\n\n# c\nrich==13.0\n")
    assert audit.packages == ["pytest", "requests", "rich"]
    assert audit.duplicates == ["pytest"]
    assert audit.unpinned == ["pytest", "pytest"]


def test_repository_requirements_are_clean():
    audit = audit_requirements((REPO_ROOT / "requirements.txt").read_text(encoding="utf-8"))
    assert audit.duplicates == [] and audit.unpinned == []


def test_missing_ignore_rules():
    assert missing_ignore_rules(".venv/\n") == ["__pycache__/", ".env"]
    assert missing_ignore_rules((REPO_ROOT / ".gitignore").read_text(encoding="utf-8")) == []


def test_diagnose_lists_every_check():
    report = diagnose(REPO_ROOT)
    assert any("Python" in line for line in report)
    assert any("duplicates: none" in line for line in report)


def test_main(capsys, tmp_path):
    main(tmp_path)
    out = capsys.readouterr().out
    assert "❌ src" in out and "python -m venv .venv" in out
