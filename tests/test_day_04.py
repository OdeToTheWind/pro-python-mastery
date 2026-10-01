"""Tests for Day 04 – Variable Naming Rules."""

import pytest

from src.day_04_variable_name_rules.main import (
    MAX_LOGIN_ATTEMPTS,
    classify_style,
    format_review,
    main,
    review_name,
    to_snake_case,
)


@pytest.mark.parametrize("name", ["2fast", "my-name", "$price", "", "x²", "has space"])
def test_invalid_identifiers(name):
    review = review_name(name)
    assert not review.is_valid
    assert "identifier" in review.errors[0]


@pytest.mark.parametrize("name", ["class", "for", "None", "async"])
def test_hard_keywords_are_errors(name):
    assert review_name(name).errors == ["reserved keyword – cannot be assigned"]


@pytest.mark.parametrize("name", ["match", "case", "type"])
def test_soft_keywords_are_warnings(name):
    review = review_name(name)
    assert review.is_valid
    assert any("soft keyword" in w for w in review.warnings)


def test_builtin_shadowing_is_flagged():
    assert any("shadows the built-in max()" in w for w in review_name("max").warnings)


@pytest.mark.parametrize("name", ["l", "O", "I"])
def test_ambiguous_letters(name):
    assert any("1 or 0" in w for w in review_name(name).warnings)


def test_short_but_allowed_loop_names_have_no_length_warning():
    assert review_name("i").warnings == []
    assert any("descriptive" in w for w in review_name("ab").warnings)


def test_clean_snake_case_has_no_findings():
    review = review_name("user_age")
    assert review.is_valid and review.warnings == []


@pytest.mark.parametrize(
    ("name", "style"),
    [
        ("user_age", "snake_case"),
        ("_private_value", "snake_case"),
        ("MAX_SIZE", "CONSTANT_CASE"),
        ("HttpClient", "CapWords"),
        ("totalPrice", "mixed"),
    ],
)
def test_classify_style(name, style):
    assert classify_style(name) == style


def test_kind_specific_expectations():
    assert review_name("MAX_LOGIN_ATTEMPTS", kind="constant").warnings == []
    assert review_name("HttpClient", kind="class").warnings == []
    assert any("CONSTANT_CASE" in w for w in review_name("max_retries", kind="constant").warnings)


@pytest.mark.parametrize(
    ("given", "expected"),
    [("totalPrice", "total_price"), ("HTTPServerError", "http_server_error"), ("my-name", "my_name")],
)
def test_to_snake_case(given, expected):
    assert to_snake_case(given) == expected


def test_camel_case_warning_suggests_fix():
    assert "'total_price'" in review_name("totalPrice").warnings[-1]


def test_constant_value_and_format():
    assert MAX_LOGIN_ATTEMPTS == 3
    assert format_review(review_name("user_age")).startswith("✅")
    assert format_review(review_name("2x")).startswith("❌")


def test_main_interactive_loop(capsys, scripted_input):
    scripted_input(["fooBar", ""])
    main()
    out = capsys.readouterr().out
    assert "'foo_bar'" in out
    assert "x²" in out
