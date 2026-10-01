"""Tests for Day 19 – Nested Collections."""

import pytest

from src.day_19_nested_collections.main import (
    RECORDS,
    add_score,
    build_gradebook,
    class_report,
    deep_get,
    main,
    student_average,
    subject_scores,
    subject_toppers,
)


@pytest.fixture
def book():
    return build_gradebook(RECORDS)


def test_build_gradebook_shape(book):
    assert book["10A"]["Aarav"] == {"math": [92, 88], "science": [79]}
    assert list(book) == ["10A", "10B"]


def test_add_score_creates_levels_and_validates():
    book = {}
    add_score(book, "9C", "Zoe", "art", 100)
    assert book == {"9C": {"Zoe": {"art": [100]}}}
    with pytest.raises(ValueError):
        add_score(book, "9C", "Zoe", "art", 101)


def test_deep_get(book):
    assert deep_get(book, ["10A", "Diya", "math", 0]) == 95
    assert deep_get(book, ["10A", "Diya", "math", 5], "none") == "none"
    assert deep_get(book, ["10X"]) is None
    assert deep_get({"a": 1}, ["a", "b"], "bad") == "bad"


def test_subject_scores_dict_of_lists(book):
    assert subject_scores(book, "10A") == {"math": [92, 88, 95], "science": [79, 91]}
    assert subject_scores(book, "missing") == {}


def test_student_average(book):
    assert student_average(book, "10A", "Aarav") == 86.3
    assert student_average(book, "10A", "Nobody") is None


def test_class_report_sorted_best_first(book):
    report = class_report(book, "10A")
    assert [r["student"] for r in report] == ["Diya", "Aarav"]
    assert report[0] == {"student": "Diya", "average": 93, "subjects": ["math", "science"]}


def test_subject_toppers(book):
    assert subject_toppers(book, "10A") == {"math": "Diya", "science": "Diya"}


def test_building_does_not_share_inner_lists():
    book = build_gradebook(RECORDS)
    book["10A"]["Aarav"]["math"].append(1)
    assert build_gradebook(RECORDS)["10A"]["Aarav"]["math"] == [92, 88]


def test_main(capsys):
    main()
    assert "Deep get missing → n/a" in capsys.readouterr().out
