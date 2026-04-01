# tests/test_day_18.py
import pytest
from src.day_18_dictionaries_lists.main import student_info, create_order


def test_student_info():
    result = student_info("Aarav", 16, grade="11th", city="Bengaluru")
    assert "Aarav" in result
    assert "16" in result
    assert "11th" in result
    assert "Bengaluru" in result


def test_student_info_defaults():
    result = student_info("Priya", 15)
    assert "Priya" in result
    assert "10th" in result  # default grade
    assert "Unknown" in result  # default city


def test_create_order():
    order = create_order("Meera", item="Laptop", price=65000, quantity=1)
    assert order["customer"] == "Meera"
    assert order["item"] == "Laptop"
    assert order["price"] == 65000


def test_create_order_minimal():
    order = create_order("Rahul")
    assert order["customer"] == "Rahul"
    assert len(order) == 1