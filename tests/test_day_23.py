# tests/test_day_23.py
import pytest

def outer_with_nonlocal():
    count = 0
    def inner():
        nonlocal count
        count += 1
        return count
    return inner


def test_nonlocal_behavior():
    counter = outer_with_nonlocal()
    assert counter() == 1
    assert counter() == 2
    assert counter() == 3


def test_local_scope():
    x = 100
    def inner():
        x = 200  # local variable
        return x
    assert inner() == 200
    assert x == 100  # outer x unchanged


def test_global_scope_simulation():
    # Simulate global behavior safely
    global_var = 10
    def modify():
        nonlocal global_var   # in real global we would use global keyword
        global_var += 5
        return global_var
    assert modify() == 15
    assert global_var == 15


def test_le_gb_order():
    x = "global"
    def outer():
        x = "enclosing"
        def inner():
            x = "local"
            return x
        return inner()
    assert outer() == "local"
    assert x == "global"