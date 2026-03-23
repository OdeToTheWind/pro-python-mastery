# tests/test_day_09.py
import pytest
from src.day_09_logical_operations.main import check_access


@pytest.mark.parametrize(
    "age, has_ticket, is_vip, has_coupon, expected_contains",
    [
        (20, True, True, False, "VIP"),
        (25, True, False, True, "VIP"),
        (30, True, False, False, "Regular Adult"),
        (16, True, False, False, "Student/Teen"),
        (12, True, False, True, "Child with coupon"),
        (10, True, False, False, "Access Denied"),
        (22, False, True, True, "Access Denied"),
    ]
)
def test_check_access(age, has_ticket, is_vip, has_coupon, expected_contains):
    result = check_access(age, has_ticket, is_vip, has_coupon)
    assert expected_contains in result