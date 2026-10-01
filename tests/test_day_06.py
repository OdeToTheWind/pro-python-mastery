"""Tests for Day 06 – Built-in Data Types."""

import pytest

from src.day_06_data_types.main import (
    aliasing_demo,
    describe,
    format_report,
    is_hashable,
    main,
    parse_literal,
    type_check_demo,
)


@pytest.mark.parametrize(
    ("value", "type_name", "category", "mutable", "hashable"),
    [
        (42, "int", "numeric", False, True),
        (3.5, "float", "numeric", False, True),
        (True, "bool", "boolean", False, True),
        ("hi", "str", "text", False, True),
        ([1], "list", "sequence", True, False),
        ((1, 2), "tuple", "sequence", False, True),
        ({"a": 1}, "dict", "mapping", True, False),
        ({1}, "set", "set", True, False),
        (frozenset({1}), "frozenset", "set", False, True),
        (None, "NoneType", "none", False, True),
    ],
)
def test_describe(value, type_name, category, mutable, hashable):
    report = describe(value)
    assert (report.type_name, report.category, report.mutable, report.hashable) == (
        type_name,
        category,
        mutable,
        hashable,
    )


def test_tuple_containing_list_is_not_hashable():
    assert describe(([1],)).hashable is False
    assert is_hashable((1, "a")) is True


def test_length_is_none_for_unsized():
    assert describe(5).length is None
    assert describe("abc").length == 3


@pytest.mark.parametrize(
    ("text", "expected"),
    [("42", 42), ("None", None), ("[1, 'a']", [1, "a"]), ("hello world", "hello world"),
     ("__import__('os')", "__import__('os')")],
)
def test_parse_literal_is_safe(text, expected):
    assert parse_literal(text) == expected


def test_aliasing_demo():
    result = aliasing_demo()
    assert result["original"] == [1, 2, 3]
    assert result["copy"] == [1, 2]
    assert result["same object"] is True
    assert result["tuple_mutated"] is False


def test_type_vs_isinstance_for_bool():
    assert type_check_demo(True) == {"type is int": False, "isinstance int": True,
                                     "is real number": False}
    assert type_check_demo(2.5)["is real number"] is True


def test_format_report_mixed_set_does_not_crash():
    assert "set" in format_report("{1, 'a'}")


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "'None'" in out and "NoneType" in out
