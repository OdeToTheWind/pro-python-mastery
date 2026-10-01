"""Tests for Day 18 – Dictionaries and Lists."""

from decimal import Decimal

import pytest

from src.day_18_dictionaries_lists.main import (
    Cart,
    Inventory,
    OutOfStockError,
    demo_store,
    list_method_tour,
    main,
)


def test_list_method_tour():
    assert list_method_tour() == {
        "manifest": ["apples", "bread", "coffee", "eggs", "milk"],
        "popped": "rice",
        "eggs count": 1,
        "bread index": 1,
    }


def test_add_product_accumulates_stock():
    inv = Inventory()
    inv.add_product("tea", "3.00", 2)
    inv.add_product("tea", "3.20", 3)
    assert inv.stock["tea"] == 5 and inv.prices["tea"] == Decimal("3.20")
    with pytest.raises(ValueError):
        inv.add_product("tea", "1", -1)


def test_restock_and_validation():
    inv = demo_store()
    inv.restock({"bread": 7})
    assert inv.stock["bread"] == 10
    with pytest.raises(KeyError):
        inv.restock({"caviar": 1})
    with pytest.raises(ValueError):
        inv.restock({"milk": -2})


def test_discontinue_low_stock_and_value():
    inv = demo_store()
    assert inv.low_stock() == ["bread"]
    assert inv.value() == Decimal("25.70")
    assert inv.discontinue("bread") == 3
    assert "bread" not in inv.stock and "bread" not in inv.prices


def test_cart_add_merge_and_total():
    cart = Cart(demo_store())
    cart.add("milk", 2)
    cart.add("milk")
    cart.add("eggs", 6)
    assert cart.merged() == {"milk": 3, "eggs": 6}
    assert cart.total() == Decimal("5.10")


@pytest.mark.parametrize(
    ("name", "qty", "error"),
    [("milk", 0, ValueError), ("caviar", 1, KeyError), ("bread", 4, OutOfStockError)],
)
def test_cart_add_rejects(name, qty, error):
    with pytest.raises(error):
        Cart(demo_store()).add(name, qty)


def test_cart_counts_existing_lines_against_stock():
    cart = Cart(demo_store())
    cart.add("bread", 2)
    with pytest.raises(OutOfStockError):
        cart.add("bread", 2)


def test_cart_remove():
    cart = Cart(demo_store())
    cart.add("milk")
    cart.add("eggs")
    cart.add("milk")
    cart.remove("milk")
    assert cart.lines == [("eggs", 1)]
    with pytest.raises(ValueError):
        cart.remove("milk")


def test_checkout_updates_inventory_and_empties_cart():
    store = demo_store()
    cart = Cart(store)
    cart.add("eggs", 12)
    assert cart.checkout() == Decimal("3.60")
    assert store.stock["eggs"] == 12 and cart.lines == []


def test_checkout_is_all_or_nothing():
    store = demo_store()
    cart = Cart(store)
    cart.add("milk", 2)
    cart.add("bread", 3)
    store.take("bread", 2)  # someone else bought bread meanwhile
    with pytest.raises(OutOfStockError):
        cart.checkout()
    assert store.stock["milk"] == 10  # nothing was taken


def test_main(capsys):
    main()
    assert "Refused: not enough bread" in capsys.readouterr().out
