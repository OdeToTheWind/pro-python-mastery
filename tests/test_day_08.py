# tests/test_day_08.py
import pytest

# Example pure function to test (you can extract similar from main.py later)
def get_grade(score: float) -> str:
    if score < 0 or score > 100:
        return "Invalid"
    elif score >= 90:
        return "A+ / Excellent"
    elif score >= 80:
        return "A / Very Good"
    elif score >= 70:
        return "B / Good"
    elif score >= 60:
        return "C / Average"
    elif score >= 50:
        return "D / Pass"
    else:
        return "F / Needs improvement"


@pytest.mark.parametrize("score, expected", [
    (95,  "A+ / Excellent"),
    (82,  "A / Very Good"),
    (75,  "B / Good"),
    (65,  "C / Average"),
    (55,  "D / Pass"),
    (42,  "F / Needs improvement"),
    (100, "A+ / Excellent"),
    (-5,  "Invalid"),
    (101, "Invalid"),
])
def test_get_grade(score, expected):
    assert get_grade(score) == expected