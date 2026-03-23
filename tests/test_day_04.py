# tests/test_day_04.py
import pytest
from src.day_04_variable_name_rules.main import is_valid_variable_name


@pytest.mark.parametrize(
    "name, should_be_valid",
    [
        ("age", True),
        ("user_count", True),
        ("_private", True),
        ("PI", True),  # uppercase ok for constants
        ("2fast", False),
        ("my-name", False),
        ("class", False),
        ("for", False),
        ("None", False),
        ("123", False),
        ("$price", False),
        ("very_long_name_here_yes", True),
    ],
)
def test_variable_name_validation(name, should_be_valid):
    valid, _ = is_valid_variable_name(name)
    assert valid == should_be_valid, f"Failed on {name}"


def test_empty_name():
    valid, reason = is_valid_variable_name("")
    assert not valid
    assert "empty" in reason.lower()


def test_keyword_detection():
    valid, reason = is_valid_variable_name("while")
    assert not valid
    assert "keyword" in reason.lower()