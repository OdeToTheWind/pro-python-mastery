"""Tests for Day 08 – If / Elif / Else Conditionals."""

import pytest

from src.day_08_if_else_conditionals.main import (
    FALSY_EXAMPLES,
    classify_temperature,
    compare,
    hike_decision,
    is_plausible_reading,
    main,
    summarize_notes,
    truthiness,
)


def test_compare_all_operators():
    assert compare(3, 5) == {"==": False, "!=": True, "<": True, "<=": True, ">": False, ">=": False}
    assert compare(4, 4)["<="] and compare(4, 4)[">="]


@pytest.mark.parametrize(
    ("celsius", "band"),
    [(-0.1, "freezing"), (0, "cold"), (9.99, "cold"), (10, "mild"), (19.9, "mild"),
     (20, "warm"), (29.9, "warm"), (30, "hot"), (60, "hot")],
)
def test_classify_temperature_boundaries(celsius, band):
    assert classify_temperature(celsius) == band


@pytest.mark.parametrize("bad", [float("nan"), -61, 61, float("inf")])
def test_implausible_values_are_rejected(bad):
    assert not is_plausible_reading(bad)
    with pytest.raises(ValueError):
        classify_temperature(bad)


def test_freezing_needs_guide():
    assert hike_decision(-5, 0, 10, has_guide=False)[0] is False
    go, packing = hike_decision(-5, 0, 10, has_guide=True)
    assert go is True
    assert packing == ["water", "insulated jacket", "crampons"]


def test_storm_wind_blocks_everyone():
    assert hike_decision(25, 0, 60, has_guide=True)[0] is False


@pytest.mark.parametrize(("rain", "wind"), [(20, 0), (0, 40)])
def test_risky_conditions_depend_on_guide(rain, wind):
    assert hike_decision(15, rain, wind, has_guide=False)[0] is False
    assert hike_decision(15, rain, wind, has_guide=True)[0] is True


def test_hot_and_rainy_packing():
    go, packing = hike_decision(32, 1, 5, has_guide=False)
    assert go is True
    assert packing == ["water", "sun hat", "extra water", "rain shell"]


def test_truthiness():
    assert all(truthiness(v) == "falsy" for v in FALSY_EXAMPLES)
    assert truthiness([0]) == "truthy"
    assert truthiness("0") == "truthy"


def test_summarize_notes():
    assert summarize_notes("  ") == "(no notes)"
    assert summarize_notes(" bring map ") == "bring map"


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "NaN accepted? False" in out
    assert "STAY" in out and "GO" in out
