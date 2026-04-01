# tests/test_day_17.py
import pytest
from src.day_17_positional_keyword_arguments.main import (
    student_info,
    calculate_total,
    create_order,
    flexible_greeting
)


def test_student_info_positional():
    assert student_info("Rahul", 16) == "Student: Rahul, Age: 16, Grade: 10th, City: Unknown"


def test_student_info_keyword():
    result = student_info(name="Priya", age=17, city="Delhi")
    assert "Priya" in result
    assert "17" in result
    assert "Delhi" in result


def test_calculate_total_args():
    assert calculate_total(10, 20, 30) == 60
    assert calculate_total(5, 15) == 20
    assert calculate_total() == 0


def test_create_order_kwargs():
    order = create_order("Bob", product="Book", price=499, qty=2)
    assert order["customer"] == "Bob"
    assert order["product"] == "Book"
    assert order["price"] == 499


def test_flexible_greeting():
    msg = flexible_greeting("Hi", "Alice", "Bob", alice="dear", bob="sir")
    assert "Hi dear Alice" in msg
    assert "Hi sir Bob" in msg


def test_default_arguments():
    # Test that defaults work correctly
    assert "10th" in student_info("Test", 14)
    assert "Unknown" in student_info("Test", 14)