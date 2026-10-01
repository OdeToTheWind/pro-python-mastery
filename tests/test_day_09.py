"""Tests for Day 09 – Logical Operations."""

import pytest

from src.day_09_logical_operations.main import (
    ShortCircuitTracer,
    can_open,
    display_name,
    main,
    safe_ratio,
    truth_table,
    within_hours,
)


def test_truth_table():
    assert truth_table() == [
        (False, False, False, False, True),
        (False, True, False, True, True),
        (True, False, False, True, False),
        (True, True, True, True, False),
    ]


@pytest.mark.parametrize(("hour", "expected"), [(7, False), (8, True), (18, True), (19, False), (24, False), (-1, False)])
def test_within_hours_boundaries(hour, expected):
    assert within_hours(hour) is expected


def test_and_short_circuits_on_false():
    tracer = ShortCircuitTracer()
    assert tracer.evaluate_and(False, True) is False
    assert tracer.calls == ["left"]
    assert tracer.evaluate_and(True, True) is True
    assert tracer.calls == ["left", "right"]


def test_or_short_circuits_on_true():
    tracer = ShortCircuitTracer()
    assert tracer.evaluate_or(True, False) is True
    assert tracer.calls == ["left"]
    assert tracer.evaluate_or(False, False) is False
    assert tracer.calls == ["left", "right"]


@pytest.mark.parametrize(
    ("door", "role", "badge", "hour", "escorted", "expected"),
    [
        ("lobby", "visitor", False, 10, False, True),
        ("lobby", "visitor", False, 22, False, False),
        ("lobby", "staff", True, 22, False, True),
        ("lobby", "staff", False, 22, False, False),
        ("lab", "staff", True, 2, False, True),
        ("lab", "visitor", False, 10, True, True),
        ("lab", "visitor", False, 10, False, False),
        ("lab", "visitor", False, 21, True, False),
        ("server_room", "admin", True, 3, False, True),
        ("server_room", "admin", False, 10, False, False),
        ("server_room", "staff", True, 10, False, False),
    ],
)
def test_can_open(door, role, badge, hour, escorted, expected):
    assert can_open(door, role=role, has_badge=badge, hour=hour, escorted=escorted) is expected


def test_unknown_door():
    with pytest.raises(ValueError):
        can_open("roof", role="admin", has_badge=True, hour=10)


def test_or_returns_first_truthy_operand():
    assert display_name("Ada", "Ada Lovelace") == "Ada"
    assert display_name("", "Ada Lovelace") == "Ada Lovelace"
    assert display_name(None, "") == "Guest"


def test_and_guards_division():
    assert safe_ratio(0, 0) == 0.0
    assert safe_ratio(3, 4) == 0.75


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "False and ... evaluated: ['left']" in out
    assert "Welcome, Guest!" in out
