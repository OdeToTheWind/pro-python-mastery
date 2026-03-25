# tests/test_day_14.py
import pytest

# Simple functions to test block logic (extracted patterns)

def is_even(n: int) -> bool:
    if n % 2 == 0:
        return True
    else:
        return False


def count_even_numbers_up_to(n: int) -> int:
    count = 0
    for i in range(n + 1):
        if i % 2 == 0:
            count += 1
    return count


def test_is_even():
    assert is_even(4) is True
    assert is_even(7) is False


def test_count_even_numbers():
    assert count_even_numbers_up_to(10) == 6   # 0,2,4,6,8,10
    assert count_even_numbers_up_to(5) == 3    # 0,2,4
    assert count_even_numbers_up_to(0) == 1    # 0


def test_nested_block_logic():
    # Simple test for nested if + for pattern
    result = []
    for i in range(5):
        if i % 2 == 0:
            result.append(i * 2)
    assert result == [0, 4, 8]