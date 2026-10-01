"""Tests for Day 33 – Module Aliasing."""

import datetime
import json
import statistics
import tomllib
from collections import Counter

import pytest

from src.day_33_module_aliasing import main as day33


def test_aliases_point_to_the_real_objects():
    assert day33.dt is datetime
    assert day33.stats is statistics
    assert day33.Tally is Counter
    assert day33.json_loads is json.loads
    assert day33.toml_loads is tomllib.loads
    assert day33.json_loads is not day33.toml_loads


def test_resolve_aliases():
    resolved = day33.resolve_aliases()
    assert resolved["dt"] == "datetime"
    assert resolved["Tally"] == "collections.Counter"
    assert resolved["toml_loads"].startswith("tomllib.")  # implemented in a private submodule


def test_load_settings_merges_and_toml_wins():
    merged = day33.load_settings('{"goal": 1, "device": "w"}', "goal = 2")
    assert merged == {"goal": 2, "device": "w"}


def test_weekly_summary():
    summary = day33.weekly_summary({"Mon": 9000, "Tue": 3000, "Wed": 12000}, datetime.date(2026, 4, 13))
    assert summary == {"range": "13 Apr – 19 Apr", "mean": 8000, "median": 9000,
                       "best_day": "Wed", "active_days": 2}


def test_weekly_summary_empty():
    with pytest.raises(ValueError):
        day33.weekly_summary({}, datetime.date(2026, 1, 1))


def test_alias_guide_flags_single_letter_alias():
    assert "avoid" in day33.ALIAS_GUIDE["import math as m"]


def test_main(capsys):
    day33.main()
    assert "json_loads  → json.loads" in capsys.readouterr().out
