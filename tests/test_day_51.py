# tests/test_day_51.py
import pytest

def test_custom_exception():
    with pytest.raises(ValueError):
        age = -5
        if age < 0:
            raise ValueError("Age cannot be negative")