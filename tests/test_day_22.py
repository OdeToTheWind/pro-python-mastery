# tests/test_day_22.py
import pytest
from src.day_22_doc_string_vs_comments.main import add_numbers, calculate_bmi


def test_add_numbers_docstring_exists():
    """Ensure the function has a proper docstring"""
    assert add_numbers.__doc__ is not None
    assert "Add two numbers" in add_numbers.__doc__


def test_calculate_bmi_docstring_exists():
    assert calculate_bmi.__doc__ is not None
    assert "Body Mass Index" in calculate_bmi.__doc__


def test_add_numbers_functionality():
    assert add_numbers(10, 20) == 30
    assert add_numbers(-5, 5) == 0


def test_calculate_bmi_functionality():
    assert calculate_bmi(70, 1.75) == 22.86
    with pytest.raises(ValueError):
        calculate_bmi(70, 0)


def test_docstring_contains_args_and_returns():
    doc = add_numbers.__doc__
    assert "Args:" in doc or "args:" in doc.lower()
    assert "Returns:" in doc or "returns:" in doc.lower()