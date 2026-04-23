# tests/test_day_34.py
from src.day_34_optional_required_default_parameters.main import create_user, calculate_price

def test_create_user():
    user = create_user("Alice", 25)
    assert user["name"] == "Alice"
    assert user["email"] == "not provided"
    assert user["is_active"] is True

def test_calculate_price():
    assert calculate_price(1000) == 1180.0          # 18% tax
    assert calculate_price(1000, quantity=2) == 2360.0
    assert calculate_price(1000, discount=0.1) == 1062.0