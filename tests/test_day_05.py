"""Tests for Day 05 – Mathematical Operations."""

from decimal import Decimal

import pytest

from src.day_05_math_operations.main import (
    calculate,
    floor_division_facts,
    main,
    precedence_examples,
    safe_divide,
    split_bill,
)


@pytest.mark.parametrize(
    ("a", "op", "b", "expected"),
    [
        (10, "+", 3, 13),
        (10, "-", 3, 7),
        (10, "*", 3, 30),
        (10, "/", 4, 2.5),
        (10, "//", 3, 3),
        (-7, "//", 2, -4),
        (-7, "%", 2, 1),
        (2, "**", 10, 1024),
    ],
)
def test_calculate(a, op, b, expected):
    assert calculate(a, op, b) == pytest.approx(expected)


def test_float_floor_division_returns_float():
    assert calculate(10.0, "//", 3.0) == 3.0
    assert isinstance(calculate(10.0, "//", 3.0), float)


@pytest.mark.parametrize("op", ["/", "//", "%"])
def test_division_by_zero_raises(op):
    with pytest.raises(ZeroDivisionError):
        calculate(1, op, 0)


@pytest.mark.parametrize(("a", "op", "b"), [(1, "^", 2), (10, "**", 5000), (-8, "**", 0.5)])
def test_invalid_operations_raise_value_error(a, op, b):
    with pytest.raises(ValueError):
        calculate(a, op, b)


def test_overflow_is_raised_not_hidden():
    with pytest.raises(OverflowError):
        calculate(10.0, "**", 400)


def test_safe_divide():
    assert safe_divide(9, 3) == 3
    assert safe_divide(1, 0) is None
    assert safe_divide(1, 0, default=0.0) == 0.0


@pytest.mark.parametrize(("a", "b"), [(7, 2), (-7, 2), (7, -2), (-7, -2)])
def test_floor_division_identity(a, b):
    facts = floor_division_facts(a, b)
    assert facts["identity holds"] is True
    assert facts["a // b"] <= facts["a / b"]


def test_floor_vs_truncation_differs_for_negatives():
    facts = floor_division_facts(-7, 2)
    assert (facts["a // b"], facts["int(a / b)"]) == (-4, -3)


def test_precedence_examples_values():
    table = dict(precedence_examples())
    assert table["2 + 3 * 4"] == 14
    assert table["-2 ** 2"] == -4
    assert table["2 ** 3 ** 2"] == 512


def test_split_bill_shares_add_up_exactly():
    shares = split_bill("100.00", 3)
    assert shares == [Decimal("33.34"), Decimal("33.33"), Decimal("33.33")]
    assert sum(shares) == Decimal("100.00")


def test_split_bill_with_tip_and_validation():
    assert sum(split_bill("80", 4, tip_percent=15)) == Decimal("92.00")
    with pytest.raises(ValueError):
        split_bill("10", 0)


def test_main_calculator(capsys, scripted_input):
    scripted_input(["7 // 2", "1 / 0", "bad", ""])
    main()
    out = capsys.readouterr().out
    assert "= 3.0" in out
    assert "ZeroDivisionError" in out
    assert "ValueError" in out
