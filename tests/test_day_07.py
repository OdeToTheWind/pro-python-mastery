# tests/test_day_07.py
import pytest
from src.day_07_converting_types.main import (
    pre_convert_to_intended,
    attempt_final_conversion
)


@pytest.mark.parametrize("raw, intended, expected_type, expect_error", [
    ("123",   "int",    int,   False),
    ("12.5",  "float",  float, False),
    ("hello", "int",    str,   True),   # stays str, error
    ("True",  "bool",   bool,  False),
    ("0",     "bool",   bool,  False),
    ("",      "bool",   bool,  False),
    ("abc",   "str",    str,   False),
])
def test_pre_convert(raw, intended, expected_type, expect_error):
    value, err = pre_convert_to_intended(raw, intended)
    if expect_error:
        assert err is not None
        assert isinstance(value, str)
    else:
        assert err is None
        assert isinstance(value, expected_type)


@pytest.mark.parametrize("value, target, expect_success", [
    (123,   "str",   True),
    ("456", "int",   True),
    (True,  "int",   True),
    (42,    "list",  False),
])
def test_final_convert(value, target, expect_success):
    res, err = attempt_final_conversion(value, target)
    if expect_success:
        assert err is None
        assert res is not None
    else:
        assert err is not None