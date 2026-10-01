"""Tests for Day 41 – File I/O (always in tmp_path, never the working tree)."""

from datetime import date
from pathlib import Path

import pytest

from src.day_41_file_io import main as day41
from src.day_41_file_io.main import (
    append_entry,
    atomic_write,
    create_new,
    default_journal_path,
    iter_entries,
    read_entries,
    search,
    write_entries,
)


def test_write_then_append_keeps_lines_separate(tmp_path):
    journal = tmp_path / "j.txt"
    write_entries(journal, ["first"])
    append_entry(journal, "second", date(2026, 1, 2))
    assert journal.read_text(encoding="utf-8") == "first\n2026-01-02 second\n"


def test_write_overwrites(tmp_path):
    journal = tmp_path / "j.txt"
    write_entries(journal, ["a", "b"])
    write_entries(journal, ["c"])
    assert read_entries(journal) == ["c"]


def test_entries_are_normalised_and_validated(tmp_path):
    journal = tmp_path / "nested" / "j.txt"
    write_entries(journal, ["  spaced   out  "])
    assert read_entries(journal) == ["spaced out"]
    with pytest.raises(ValueError):
        append_entry(journal, "   ")


def test_unicode_round_trip(tmp_path):
    journal = tmp_path / "j.txt"
    write_entries(journal, ["café ☕ – naïve"])
    assert read_entries(journal) == ["café ☕ – naïve"]


def test_read_missing_file_is_empty(tmp_path):
    assert read_entries(tmp_path / "missing.txt") == []


def test_iter_entries_is_lazy(tmp_path):
    journal = tmp_path / "j.txt"
    write_entries(journal, ["x", "y"])
    stream = iter_entries(journal)
    assert next(stream) == "x"


def test_create_new_does_not_overwrite(tmp_path):
    target = tmp_path / "new.txt"
    assert create_new(target, "one") is True
    assert create_new(target, "two") is False
    assert target.read_text(encoding="utf-8") == "one"


def test_atomic_write_replaces_and_cleans_up(tmp_path):
    target = tmp_path / "data.txt"
    target.write_text("old", encoding="utf-8")
    atomic_write(target, "new")
    assert target.read_text(encoding="utf-8") == "new"
    assert list(tmp_path.iterdir()) == [target]


def test_atomic_write_keeps_old_file_on_failure(tmp_path, monkeypatch):
    target = tmp_path / "data.txt"
    target.write_text("old", encoding="utf-8")

    def broken_replace(_src, _dst):
        raise OSError("disk full")

    monkeypatch.setattr(day41.os, "replace", broken_replace)
    with pytest.raises(OSError):
        atomic_write(target, "new")
    assert target.read_text(encoding="utf-8") == "old"
    assert list(tmp_path.iterdir()) == [target]


def test_search(tmp_path):
    journal = tmp_path / "j.txt"
    write_entries(journal, ["Python rocks", "tea time", "more python"])
    assert search(journal, "PYTHON") == [(1, "Python rocks"), (3, "more python")]


def test_default_path_is_git_ignored_data_dir():
    assert default_journal_path().parent.name == ".data"


def test_main(capsys, tmp_path):
    day41.main(tmp_path / "journal.txt")
    out = capsys.readouterr().out
    assert "Create again with mode 'x': False" in out
    assert "Backup lines: 3" in out
    assert Path(tmp_path / "journal.bak").exists()
