"""Tests for Day 49 – Strongly Dynamic Typing."""

import pytest

from src.day_49_strongly_dynamic_typing.main import (
    add_quantities,
    enforce_types,
    hints_not_enforced,
    main,
    rebinding_demo,
    restock,
    strong_typing_errors,
    total_length,
)


def test_dynamic_rebinding():
    assert rebinding_demo() == ["int", "str", "list"]


def test_strong_typing():
    results = strong_typing_errors()
    assert results['"3" + 4'] == "TypeError"
    assert results["[1] + (2,)"] == "TypeError"
    assert results['"5" * "2"'] == "TypeError"
    assert results["None + 1"] == "TypeError"
    assert results['"3" * 4'] == "'3333'"
    assert results["True + 1"] == "2"


def test_add_quantities_explicit_conversion():
    assert add_quantities(" 3 ", 4) == 7
    with pytest.raises(ValueError, match="cannot add"):
        add_quantities("three", 4)


def test_duck_typing():
    assert total_length("abc", [1, 2], {"k": 1}, 7, None) == 3 + 2 + 1 + 1 + 1


def test_hints_are_not_enforced_by_interpreter():
    assert hints_not_enforced().startswith("ValueError raised by the f-string")


def test_enforce_types_decorator():
    assert restock("A", 2) == "A: +2"
    with pytest.raises(TypeError, match="quantity must be int, got str"):
        restock("A", "2")
    with pytest.raises(TypeError):
        restock(sku=1, quantity=2)


def test_enforce_types_ignores_complex_hints():
    @enforce_types
    def f(items: list[int], name: str = "x") -> int:
        return len(items)

    assert f(["not", "checked"]) == 2  # generic hints are skipped, plain classes are checked
    assert f.__name__ == "f"


def test_main(capsys):
    main()
    assert "rejected: quantity must be int, got str" in capsys.readouterr().out
