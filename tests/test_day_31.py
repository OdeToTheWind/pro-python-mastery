"""Tests for Day 31 – Python Methods."""

from decimal import Decimal

import pytest

from src.day_31_python_methods.main import GlutenFreePizza, Pizza, main, temporary_base_price


def test_instance_method_chaining_and_price():
    pizza = Pizza("small").add_topping(" Olives ").add_topping("ham")
    assert pizza.toppings == ["olives", "ham"]
    assert pizza.price() == Decimal("8.80")  # 8 × 0.8 + 2 × 1.20


@pytest.mark.parametrize("topping", ["", "olives"])
def test_add_topping_validation(topping):
    pizza = Pizza(toppings=["olives"])
    with pytest.raises(ValueError):
        pizza.add_topping(topping)


def test_instances_do_not_share_topping_lists():
    a, b = Pizza(), Pizza()
    a.add_topping("ham")
    assert b.toppings == []


def test_alternative_constructors():
    assert Pizza.margherita("large").toppings == ["tomato", "mozzarella", "basil"]
    assert Pizza.from_dict({"toppings": ("corn",)}).size == "medium"


def test_classmethod_returns_subclass():
    pizza = GlutenFreePizza.margherita()
    assert type(pizza) is GlutenFreePizza
    assert pizza.price() == Decimal("13.10")  # 9.50 + 3 × 1.20


def test_set_base_price_changes_all_instances_and_is_restored():
    pizza = Pizza()
    with temporary_base_price(Decimal("6")):
        assert pizza.price() == Decimal("6.00")
    assert Pizza.base_price == Decimal("8.00")
    with pytest.raises(ValueError):
        Pizza.set_base_price(Decimal("0"))


def test_static_methods_callable_from_class_and_instance():
    assert Pizza.valid_size("large") and not Pizza.valid_size("huge")
    assert Pizza().valid_size("small")
    assert Pizza.format_price(Decimal("5")) == "€5.00"
    with pytest.raises(ValueError):
        Pizza("huge")


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "Happy hour medium margherita: €9.60" in out
    assert Pizza.base_price == Decimal("8.00")
