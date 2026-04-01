# tests/test_day_15.py
import pytest

def countdown_steps(start: int) -> int:
    """Simulate countdown and return how many steps were taken"""
    steps = 0
    count = start
    while count > 0:
        steps += 1
        count -= 1
    return steps


def find_number(target: int, max_val: int = 10) -> bool:
    """Return True if number is found"""
    i = 1
    while i <= max_val:
        if i == target:
            return True
        i += 1
    return False


def test_countdown():
    assert countdown_steps(5) == 5
    assert countdown_steps(0) == 0
    assert countdown_steps(1) == 1


def test_find_number():
    assert find_number(7) is True
    assert find_number(12) is False
    assert find_number(5, max_val=3) is False


def test_while_else_behavior():
    # If break occurs, else should not run (simulated)
    found = find_number(3)
    assert found is True