# tests/test_day_21.py
import pytest
from src.day_21_return_vs_print.main import (
    add_with_return,
    calculate_final_price
)


def test_add_with_return():
    assert add_with_return(10, 20) == 30
    assert add_with_return(5.5, 3.2) == 8.7
    assert add_with_return(-10, 10) == 0


def test_calculate_final_price():
    assert calculate_final_price(1000) == 1180.0      # 18% tax
    assert calculate_final_price(5000) == 5900.0
    assert calculate_final_price(100) == 118.0


def test_calculate_final_price_rounding():
    result = calculate_final_price(123.456)
    assert result == 145.68   # properly rounded to 2 decimal places


def test_return_behavior():
    """Test that the function actually returns a value (not None)"""
    result = add_with_return(100, 200)
    assert result is not None
    assert isinstance(result, (int, float))
    assert result == 300