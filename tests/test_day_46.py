"""Tests for Day 46 – Dictionary Comprehensions."""

from decimal import Decimal

import pytest

from src.day_46_dictionary_comprehensions.main import (
    CATALOGUE,
    apply_discount,
    filter_items,
    index_by,
    invert,
    main,
    merge_prices,
    price_list,
    stock_matrix,
    word_frequencies,
)


def test_index_by():
    index = index_by(CATALOGUE, "isbn")
    assert list(index) == ["111", "222", "333", "444"]
    assert index["222"]["title"] == "Dune"


def test_price_list_requires_equal_lengths():
    assert price_list(["a"], [Decimal("1")]) == {"a": Decimal("1")}
    with pytest.raises(ValueError):
        price_list(["a", "b"], [Decimal("1")])


def test_apply_discount_does_not_mutate_input():
    prices = {"a": Decimal("10.00"), "b": Decimal("8.99")}
    assert apply_discount(prices, 15) == {"a": Decimal("8.50"), "b": Decimal("7.64")}
    assert prices["a"] == Decimal("10.00")
    with pytest.raises(ValueError):
        apply_discount(prices, 120)


def test_filter_items():
    assert filter_items({"a": 0, "b": 3, "c": 1}, lambda n: n > 0) == {"b": 3, "c": 1}


def test_invert_keeps_duplicates():
    assert invert({"Fluent": "tech", "Dune": "sci-fi", "Clean": "tech"}) == {
        "tech": ["Fluent", "Clean"],
        "sci-fi": ["Dune"],
    }
    assert invert({}) == {}


def test_stock_matrix_nested():
    assert stock_matrix(CATALOGUE) == {
        "classic": {"Emma": 2},
        "sci-fi": {"Dune": 0},
        "tech": {"Fluent Python": 4, "Clean Code": 7},
    }


def test_word_frequencies_sorted_by_count_then_word():
    assert word_frequencies("The cat and the hat. THE end!") == {"the": 3, "and": 1, "cat": 1, "end": 1, "hat": 1}
    assert word_frequencies("a an", min_length=3) == {}


def test_merge_prices_later_wins():
    assert merge_prices({"a": Decimal("1")}, {"a": Decimal("2"), "b": Decimal("3")}) == {
        "a": Decimal("2"), "b": Decimal("3")}


def test_main(capsys):
    main()
    assert "'great': 3" in capsys.readouterr().out
