"""Tests for scripts/learn.py – the per-day study mode behind ./propython.sh <day>."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import learn  # noqa: E402

PLAIN = learn.Style(enabled=False)


@pytest.mark.parametrize("day", range(1, 101))
def test_every_day_can_be_explained(day, capsys):
    learn.explain(day, PLAIN)
    out = capsys.readouterr().out
    assert f"Day {day} · " in out and "▸ Where each skill lives in the code" in out
    assert "src/day_" in out and "▸ Pitfalls to avoid" in out and "tests prove" in out


def test_explain_shows_code_locations_and_notes(capsys):
    learn.explain(47, PLAIN)
    out = capsys.readouterr().out
    assert "src/day_47_packing_unpacking/main.py:" in out
    assert "split_route(route: list[str])" in out  # signature without quote noise
    assert "Phase 2 · Intermediate Python (Days 25–56)" in out
    assert "✓ extended unpacking" in out


def test_locate_handles_constants_and_methods():
    import importlib

    day83 = importlib.import_module("src.day_83_robust_cli_application.main")
    where, summary = learn.locate(day83, "EXIT_CODES")
    assert where.endswith("(constant)") and summary.startswith("EXIT_CODES = {")
    where, summary = learn.locate(day83, "HabitStore.save")
    assert ":" in where and summary.startswith("HabitStore.save(self)")


def test_style_colours_only_when_enabled():
    assert learn.Style(True).title("x") == "\033[1;36mx\033[0m"
    assert PLAIN.title("x") == "x"


def test_ask_day_validates_and_quits(monkeypatch, capsys):
    answers = iter(["zero", "150", "12"])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    assert learn.ask_day() == 12
    assert capsys.readouterr().out.count("whole number from 1 to 100") == 2
    monkeypatch.setattr("builtins.input", lambda _prompt: "q")
    assert learn.ask_day() is None

    def closed(_prompt):
        raise EOFError

    monkeypatch.setattr("builtins.input", closed)
    assert learn.ask_day() is None and learn.ask_yes("?") is False


def test_main_explains_without_running_tests(capsys):
    assert learn.main(["5", "--no-tests"]) == 0
    out = capsys.readouterr().out
    assert "Day 5 · " in out and "▸ Try it yourself" in out and "./propython.sh 5" in out
    assert "Running tests" not in out


def test_main_rejects_unknown_day(capsys):
    assert learn.main(["101", "--no-tests"]) == 2
    assert "no Day 101" in capsys.readouterr().err


def test_main_runs_the_day_tests(monkeypatch, capsys):
    calls = []
    monkeypatch.setattr(learn.subprocess, "run",
                        lambda cmd, **kw: calls.append(cmd) or type("R", (), {"returncode": 0})())
    assert learn.main(["2", "--demo"]) == 0
    assert any("tests/test_day_02.py" in part for part in calls[0])
    assert calls[1][-1].startswith("src.day_02_") and calls[1][-1].endswith(".main")
