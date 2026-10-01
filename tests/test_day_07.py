"""Tests for Day 07 – Converting Types."""

import pytest

from src.day_07_converting_types.main import (
    convert,
    error_examples,
    main,
    parse_bool,
    parse_collection,
)


@pytest.mark.parametrize(
    ("value", "target", "expected"),
    [
        ("42", "int", 42),
        ("12.5", "float", 12.5),
        (7, "str", "7"),
        ("no", "bool", False),
        ("YES", "bool", True),
        ("abc", "list", ["a", "b", "c"]),
        ("[1, 2, 2]", "set", {1, 2}),
        ("(1, 2)", "list", [1, 2]),
        ("[('a', 1)]", "dict", {"a": 1}),
        ([("k", "v")], "dict", {"k": "v"}),
        (True, "int", 1),
    ],
)
def test_successful_conversions(value, target, expected):
    result = convert(value, target)
    assert result.ok and result.value == expected


@pytest.mark.parametrize(
    ("value", "target", "error_type"),
    [
        ("12.5", "int", "ValueError"),
        ("hello", "float", "ValueError"),
        ("maybe", "bool", "ValueError"),
        (None, "int", "TypeError"),
        (42, "list", "TypeError"),
        (float("inf"), "int", "OverflowError"),
        ("[1,", "list", "SyntaxError"),
        ("1", "complex", "KeyError"),
    ],
)
def test_failed_conversions_report_exact_error(value, target, error_type):
    result = convert(value, target)
    assert not result.ok
    assert result.error_type == error_type


def test_bool_pitfall_is_handled():
    assert bool("False") is True  # the trap
    assert parse_bool("False") is False  # the fix
    with pytest.raises(ValueError):
        parse_bool("perhaps")


def test_parse_collection():
    assert parse_collection("{'a': 1}", "dict") == {"a": 1}
    assert parse_collection("[3, 1]", "tuple") == (3, 1)


def test_error_examples_distinguish_value_and_type_errors():
    outcome = error_examples()
    assert outcome["int('abc')"] == "ValueError"
    assert outcome["int([1, 2])"] == "TypeError"
    assert outcome["float(None)"] == "TypeError"
    assert outcome["dict([1, 2])"] == "TypeError"
    assert outcome["dict(['ab', 'cd'])"] == "ok → {'a': 'b', 'c': 'd'}"
    assert outcome["int(float('inf'))"] == "OverflowError"


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "bool('False') is True" in out
