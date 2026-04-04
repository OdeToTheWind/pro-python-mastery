# tests/test_day_24.py
import pytest

def safe_average(numbers):
    """Example function with proper error handling (for testing)"""
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


def test_safe_average():
    assert safe_average([10, 20, 30]) == 20
    assert safe_average([]) is None


def test_bug_patterns():
    # Test common bug pattern: division by zero avoidance
    def safe_divide(a, b):
        if b == 0:
            return None
        return a / b
    
    assert safe_divide(10, 2) == 5
    assert safe_divide(10, 0) is None