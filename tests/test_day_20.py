"""Tests for Day 20 – Returning Functions."""

import pytest

from src.day_20_returning_functions.main import (
    collapse_spaces,
    compose,
    main,
    make_excerpt,
    make_truncator,
    reading_time,
    strip_markdown,
    text_stats,
    validate_title,
)


@pytest.mark.parametrize(("words", "minutes"), [(0, 0), (1, 1), (200, 1), (201, 2)])
def test_reading_time_rounds_up(words, minutes):
    assert reading_time(words) == minutes


def test_reading_time_rejects_negative():
    with pytest.raises(ValueError):
        reading_time(-1)


def test_text_stats_returns_tuple():
    result = text_stats("Hi there. I'm here!")
    assert isinstance(result, tuple)
    words, sentences, avg = result
    assert (words, sentences, avg) == (4, 2, 3.5)  # (2 + 5 + 3 + 4) / 4


def test_text_stats_empty_input():
    assert text_stats("") == (0, 0, 0.0)
    assert text_stats("...") == (0, 0, 0.0)


@pytest.mark.parametrize(
    ("title", "valid", "reason"),
    [
        ("", False, "title is empty"),
        ("x" * 71, False, "title longer than 70 characters"),
        (" Hi", False, "title has leading or trailing spaces"),
        ("lower case", False, "title should start with a capital letter"),
        ("Good Title", True, "ok"),
    ],
)
def test_validate_title_guard_clauses(title, valid, reason):
    assert validate_title(title) == (valid, reason)


def test_make_truncator_returns_independent_functions():
    short, long = make_truncator(6), make_truncator(20)
    assert short("abcdefgh") == "abcde…"
    assert long("abcdefgh") == "abcdefgh"
    assert short("abc") == "abc"
    with pytest.raises(ValueError):
        make_truncator(1)


def test_compose_order_is_left_to_right():
    pipeline = compose(str.strip, str.upper, lambda s: s + "!")
    assert pipeline("  hi ") == "HI!"
    assert compose()("same") == "same"


def test_pipeline_helpers():
    assert collapse_spaces(" a \n b ") == "a b"
    assert strip_markdown("# *Hi* `x`") == " Hi x"


def test_make_excerpt():
    excerpt = make_excerpt("# Title\n\n**Bold** text   with   spaces " * 3)
    assert len(excerpt) <= 40 and excerpt.endswith("…")
    assert "*" not in excerpt and "  " not in excerpt


def test_main(capsys):
    main()
    assert "words=11 sentences=4" in capsys.readouterr().out
