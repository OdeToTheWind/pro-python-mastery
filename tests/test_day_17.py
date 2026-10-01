"""Tests for Day 17 – Positional and Keyword Arguments."""

import pytest

from src.day_17_positional_keyword_arguments.main import (
    boarding_announcement,
    book_flight,
    how_arguments_bind,
    main,
    parameter_kinds,
)


def test_defaults():
    booking = book_flight("lhr", "jfk")
    assert booking == {"route": "LHR→JFK", "passengers": 1, "cabin": "economy",
                       "flexible": False, "total": 120.0}


def test_passengers_positional_or_keyword():
    assert book_flight("A", "B", 2) == book_flight("A", "B", passengers=2)


def test_keyword_only_options():
    assert book_flight("A", "B", cabin="business", flexible=True)["total"] == pytest.approx(441.6)


def test_positional_only_cannot_be_named():
    with pytest.raises(TypeError):
        book_flight(origin="A", destination="B")  # type: ignore[call-arg]


def test_keyword_only_cannot_be_positional():
    with pytest.raises(TypeError):
        book_flight("A", "B", 1, "business")  # type: ignore[misc]


@pytest.mark.parametrize(
    "kwargs", [{"passengers": 0}, {"cabin": "first"}],
)
def test_validation(kwargs):
    with pytest.raises(ValueError):
        book_flight("A", "B", **kwargs)


def test_same_origin_and_destination():
    with pytest.raises(ValueError):
        book_flight("lhr", "LHR")


def test_parameter_kinds():
    kinds = parameter_kinds(book_flight)
    assert kinds["origin"] == "positional-only"
    assert kinds["passengers"] == "positional or keyword"
    assert kinds["cabin"] == "keyword-only"


def test_how_arguments_bind_applies_defaults():
    bound = how_arguments_bind(book_flight, "DEL", "BLR", passengers=3)
    assert bound["passengers"] == 3 and bound["cabin"] == "economy"


def test_boarding_announcement_no_double_spaces():
    assert boarding_announcement("Ada", "Bob", bob="Mr.") == [
        "Welcome aboard, Ada!",
        "Welcome aboard, Mr. Bob!",
    ]


def test_boarding_announcement_greeting_is_not_swallowed():
    assert boarding_announcement("Alice", "Bob")[0] == "Welcome aboard, Alice!"
    assert boarding_announcement(greeting="Hi") == ["Hi, everyone!"]


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert out.count("TypeError for") == 2
    assert "Namaste, Dr. Diya!" in out
