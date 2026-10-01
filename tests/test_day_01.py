"""Tests for Day 01 – Variables, Type Hinting & Scoping."""

import typing

import pytest

from src.day_01_variables import main as day01


@pytest.fixture(autouse=True)
def _reset_global_total():
    day01.reset_sessions()
    yield
    day01.reset_sessions()


def test_first_or_default_returns_first_item():
    assert day01.first_or_default([3, 4], 0) == 3
    assert day01.first_or_default("xyz", "?") == "x"


def test_first_or_default_falls_back_on_empty():
    assert day01.first_or_default([], "empty") == "empty"


def test_pep695_type_parameters_are_declared():
    (param,) = day01.first_or_default.__type_params__
    assert isinstance(param, typing.TypeVar)
    assert param.__name__ == "T"
    assert isinstance(day01.Minutes, typing.TypeAliasType)


def test_format_status_uses_alignment_and_padding():
    line = day01.format_status("Ada", 7, 1500, active=False)
    assert line.startswith("Ada         |")
    assert "day 007" in line
    assert "1,500 min" in line
    assert line.endswith("'paused'")


def test_record_session_updates_global_total():
    assert day01.record_session(20) == 20
    assert day01.record_session(15) == 35
    assert day01.total_minutes == 35


def test_record_session_rejects_negative_minutes():
    with pytest.raises(ValueError):
        day01.record_session(-1)


def test_streak_counter_uses_independent_enclosing_state():
    first, second = day01.make_streak_counter(), day01.make_streak_counter()
    assert [first(True), first(True), first(False), first(True)] == [1, 2, 0, 1]
    assert second(True) == 1  # each closure has its own `streak`


def test_shadowing_does_not_change_global():
    inside, outside = day01.shadowing_demo()
    assert inside == "local label"
    assert outside == "global label" == day01.label


def test_summarize_handles_empty_log():
    assert day01.summarize([]) == "0 sessions, 0.0 h total, first topic: nothing yet"


def test_main_prints_walkthrough(capsys):
    day01.main()
    out = capsys.readouterr().out
    assert "Global total after record_session(): 125 min" in out
    assert "[1, 2, 0, 1]" in out
