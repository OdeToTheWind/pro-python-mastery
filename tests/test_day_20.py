# tests/test_day_20.py
import pytest
from src.day_20_returning_functions.main import (
    calculate_statistics,
    get_grade_with_feedback,
    is_valid_password
)


def test_calculate_statistics():
    stats = calculate_statistics([10, 20, 30, 40])
    assert stats == (100, 25.0, 10, 40)


def test_calculate_statistics_empty():
    stats = calculate_statistics([])
    assert stats == (0, 0, 0, 0)


def test_get_grade_with_feedback():
    grade, feedback = get_grade_with_feedback(92)
    assert grade == "A+"
    assert "Excellent" in feedback
    
    grade, feedback = get_grade_with_feedback(45)
    assert grade == "F"
    assert "harder" in feedback


def test_is_valid_password():
    valid, msg = is_valid_password("Python2025")
    assert valid is True
    assert msg == "Strong password!"
    
    valid, msg = is_valid_password("short")
    assert valid is False
    assert "short" in msg.lower()
    
    valid, msg = is_valid_password("nouppercase123")
    assert valid is False


def test_early_return_behavior():
    def check_number(n):
        if n > 0:
            return "Positive"
        return "Non-positive"
    
    assert check_number(5) == "Positive"
    assert check_number(-3) == "Non-positive"