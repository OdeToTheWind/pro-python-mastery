# tests/test_day_13.py
import pytest

# Pure functions for testing (extracted logic from main.py)

def multiplication_table(n: int, limit: int = 10) -> list:
    return [n * i for i in range(1, limit + 1)]


def calculate_cart_total(cart: list) -> float:
    """cart = list of (item, price) tuples"""
    return sum(price for _, price in cart)


def test_multiplication_table():
    assert multiplication_table(5, 3) == [5, 10, 15]
    assert multiplication_table(7)[:5] == [7, 14, 21, 28, 35]


def test_cart_total():
    cart = [("apple", 30.5), ("banana", 15.0), ("milk", 50.0)]
    assert calculate_cart_total(cart) == 95.5
    assert calculate_cart_total([]) == 0.0


def test_empty_cart():
    assert calculate_cart_total([]) == 0.0