# tests/test_day_16.py
import pytest

def calculate_final_price(amount: float) -> float:
    """Simulate discount flowchart logic"""
    if amount > 10000:
        discount = 0.20
    elif amount > 5000:
        discount = 0.10
    elif amount > 2000:
        discount = 0.05
    else:
        discount = 0.0
    return round(amount * (1 - discount), 2)


def get_grade(score: float) -> str:
    """Simulate grade calculator flowchart"""
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"


def test_discount_flowchart():
    assert calculate_final_price(12000) == 9600.0   # 20% off
    assert calculate_final_price(6000) == 5400.0    # 10% off
    assert calculate_final_price(2500) == 2375.0    # 5% off
    assert calculate_final_price(1500) == 1500.0    # no discount


def test_grade_flowchart():
    assert get_grade(95) == "A+"
    assert get_grade(82) == "A"
    assert get_grade(68) == "C"
    assert get_grade(45) == "F"


def test_eligibility_flowchart_logic():
    # Simple test for age + license logic simulation
    def is_eligible(age: int, has_license: bool) -> bool:
        if age >= 18:
            return has_license
        return False
    
    assert is_eligible(20, True) is True
    assert is_eligible(20, False) is False
    assert is_eligible(16, True) is False