# tests/test_day_11.py
import pytest

def password_strength(pwd: str) -> str:
    """Example function that raises errors for testing"""
    if len(pwd) < 8:
        raise ValueError("Password too short")
    if not any(c.isdigit() for c in pwd):
        raise ValueError("Password must contain a number")
    if not any(c.isupper() for c in pwd):
        raise ValueError("Password must contain an uppercase letter")
    return "Strong"


def test_password_strength_valid():
    assert password_strength("Python2025!") == "Strong"


def test_password_strength_too_short():
    with pytest.raises(ValueError, match="too short"):
        password_strength("short")


def test_password_strength_no_number():
    with pytest.raises(ValueError, match="number"):
        password_strength("PasswordOnly")


def test_password_strength_no_upper():
    with pytest.raises(ValueError, match="uppercase"):
        password_strength("password123")