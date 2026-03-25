# tests/test_day_12.py
import pytest
from src.day_12_functions.main import (
    greet_user,
    calculate_bmi,
    calculate_grade,
    add_numbers,
    create_profile
)


def test_greet_user():
    assert greet_user("Alice") == "Hello friend Alice!"
    assert greet_user("Bob", "Dr.") == "Hello Dr. Bob!"


def test_calculate_bmi():
    assert calculate_bmi(70, 1.75) == 22.86
    with pytest.raises(ValueError):
        calculate_bmi(70, 0)


def test_calculate_grade():
    assert calculate_grade(95) == "A+"
    assert calculate_grade(82) == "A"
    assert calculate_grade(65) == "C"
    assert calculate_grade(45) == "F"


def test_add_numbers():
    assert add_numbers(1, 2, 3) == 6
    assert add_numbers(10, 20) == 30
    assert add_numbers() == 0  # no arguments


def test_create_profile():
    profile = create_profile(name="Priya", age=27, city="Bengaluru", is_student=True)
    assert profile["name"] == "Priya"
    assert profile["age"] == 27
    assert profile["is_student"] is True