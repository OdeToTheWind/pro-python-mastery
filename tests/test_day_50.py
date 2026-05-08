# tests/test_day_50.py
import pytest

def test_error_handling():
    with pytest.raises(ZeroDivisionError):
        10 / 0