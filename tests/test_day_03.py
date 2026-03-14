import pytest
from unittest.mock import patch
from src.day_03_input_output.main import get_validated_input, build_user_profile


def test_get_validated_input_valid_str():
    with patch("builtins.input", return_value="Alice"):
        result = get_validated_input("Name: ", str)
        assert result == "Alice"


def test_get_validated_input_valid_int():
    with patch("builtins.input", return_value="42"):
        result = get_validated_input("Age: ", int, min_value=0)
        assert result == 42


def test_get_validated_input_invalid_then_valid():
    with patch("builtins.input", side_effect=["abc", "25"]):
        result = get_validated_input("Age: ", int, min_value=0)
        assert result == 25


def test_get_validated_input_below_min():
    with patch("builtins.input", side_effect=["-5", "10"]):
        result = get_validated_input("Age: ", int, min_value=0)
        assert result == 10