"""Tests for Day 12 – Functions."""

import inspect
from decimal import Decimal

import pytest

from src.day_12_functions.main import (
    Drink,
    customize,
    main,
    order_total,
    price_drink,
    receipt_line,
)


@pytest.mark.parametrize(
    ("name", "size", "expected"),
    [("latte", "medium", "3.40"), ("latte", "large", "4.42"), ("espresso", "small", "1.76")],
)
def test_price_drink(name, size, expected):
    assert price_drink(name, size) == Decimal(expected)


def test_default_size_is_medium():
    assert price_drink("tea") == price_drink("tea", "medium")
    assert inspect.signature(price_drink).parameters["size"].default == "medium"


def test_unknown_menu_item():
    with pytest.raises(KeyError):
        price_drink("mocha")


def test_customize_collects_kwargs():
    drink = customize("latte", oat_milk=1, extra_shot=2)
    assert drink.extras == {"oat_milk": 1, "extra_shot": 2}
    assert drink.price == Decimal("3.40") + Decimal("0.40") + Decimal("1.20")


@pytest.mark.parametrize("extras", [{"whipped_cream": 1}, {"syrup": -1}])
def test_customize_rejects_bad_extras(extras):
    with pytest.raises(ValueError):
        customize("tea", **extras)


def test_order_total_varargs_and_tip():
    a, b = customize("tea"), customize("espresso")
    assert order_total() == Decimal("0.00")
    assert order_total(a, b) == Decimal("4.10")
    assert order_total(a, b, tip_percent=10) == Decimal("4.51")


def test_docstrings_and_type_hints_present():
    assert "Args:" in price_drink.__doc__ and "Returns:" in price_drink.__doc__
    hints = inspect.get_annotations(customize, eval_str=True)
    assert hints["return"] is Drink


def test_receipt_line_alignment():
    line = receipt_line(customize("latte", syrup=1))
    assert line.startswith("medium latte (syrup×1)")
    assert line.endswith("€  3.75")


def test_main(capsys):
    main()
    assert "Total incl. 10% tip" in capsys.readouterr().out
