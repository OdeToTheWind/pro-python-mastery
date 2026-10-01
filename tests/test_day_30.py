"""Tests for Day 30 – Getting / Setting Attributes."""

import pytest

from src.day_30_getting_setting_attributes.main import Thermostat, apply_settings, main


def test_constructor_goes_through_setter():
    with pytest.raises(ValueError):
        Thermostat("attic", 99)
    with pytest.raises(TypeError):
        Thermostat("attic", "warm")  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [5, 30, 21.5])
def test_celsius_bounds_inclusive(value):
    assert Thermostat("x", value).celsius == value


@pytest.mark.parametrize("value", [4.9, 30.1, True])
def test_celsius_rejects(value):
    t = Thermostat("x")
    with pytest.raises((ValueError, TypeError)):
        t.celsius = value


def test_fahrenheit_is_computed_and_settable():
    t = Thermostat("x", 20)
    assert t.fahrenheit == 68.0
    t.fahrenheit = 71.6
    assert t.celsius == 22.0
    with pytest.raises(ValueError):
        t.fahrenheit = 100


def test_history_is_read_only():
    t = Thermostat("x", 18)
    t.celsius = 19
    assert t.history == (18.0, 19.0)
    with pytest.raises(AttributeError):
        t.history = ()  # type: ignore[misc]


def test_schedule_deleter():
    t = Thermostat("x")
    t.schedule = "eco"
    del t.schedule
    assert t.schedule is None


def test_apply_settings_reports_each_problem():
    t = Thermostat("x")
    errors = apply_settings(t, {"celsius": 45, "history": [], "colour": "red", "_celsius": 1,
                                "fahrenheit": 64.4})
    assert t.celsius == 18.0
    assert errors[0].startswith("celsius: temperature must be between")
    assert errors[1].startswith("history:")
    assert errors[2:] == ["colour: unknown setting", "_celsius: unknown setting"]


def test_main(capsys):
    main()
    assert "22.0 °C / 71.6 °F" in capsys.readouterr().out
