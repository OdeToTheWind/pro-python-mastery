# tests/test_day_05.py
import pytest
from src.day_05_math_operations.main import perform_operation, safe_float_input


@pytest.mark.parametrize(
    "a, b, op, expected_result, expected_desc",
    [
        (10, 3, "+", 13, "Addition"),
        (10, 3, "-", 7, "Subtraction"),
        (10, 3, "*", 30, "Multiplication"),
        (10, 3, "/", 3.3333333333333335, "True Division (float result)"),
        (10, 3, "//", 3, "Floor Division (integer result)"),
        (10, 3, "%", 1, "Modulus (remainder)"),
        (2, 3, "**", 8, "Exponentiation (power)"),
        (5, 0, "/", "Error", "Division by zero is not allowed"),
        (5, 0, "//", "Error", "Division by zero is not allowed"),
        (5, 0, "%", "Error", "Division by zero is not allowed"),
    ]
)
def test_perform_operation(a, b, op, expected_result, expected_desc):
    result, desc = perform_operation(a, b, op)
    assert desc == expected_desc
    if isinstance(expected_result, str):
        assert result == expected_result
    else:
        if isinstance(result, float):
            assert abs(result - expected_result) < 1e-10
        else:
            assert result == expected_result


def test_invalid_operator():
    result, desc = perform_operation(5, 2, "xyz")
    assert result == "Unknown"
    assert desc == "Invalid operator"