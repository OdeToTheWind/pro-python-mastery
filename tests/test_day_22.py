"""Tests for Day 22 – Docstrings vs. Comments."""

import doctest
import inspect

import pytest

from src.day_22_doc_string_vs_comments import main as day22
from src.day_22_doc_string_vs_comments.main import (
    audit_docstring,
    celsius_to_gas_mark,
    function_metadata,
    grams_to_cups,
    main,
    split_comments_and_docstrings,
    undocumented,
)


def test_grams_to_cups():
    assert grams_to_cups(240, "flour") == 2.0
    assert grams_to_cups(100, "sugar") == 0.5
    with pytest.raises(ValueError):
        grams_to_cups(-1, "flour")
    with pytest.raises(ValueError):
        grams_to_cups(1, "salt")


@pytest.mark.parametrize(("celsius", "mark"), [(100, 1), (180, 4), (250, 9), (400, 9)])
def test_gas_mark(celsius, mark):
    assert celsius_to_gas_mark(celsius) == mark


def test_docstring_example_runs_as_doctest():
    finder = doctest.DocTestFinder()
    runner = doctest.DocTestRunner()
    for test in finder.find(grams_to_cups, globs=vars(day22)):
        runner.run(test)
    assert runner.summarize(verbose=False).failed == 0


def test_comments_are_not_runtime_documentation():
    assert undocumented.__doc__ is None
    assert "A comment is not documentation" in inspect.getsource(undocumented)


def test_function_metadata():
    meta = function_metadata(grams_to_cups)
    assert meta["name"] == "grams_to_cups"
    assert meta["module"] == "src.day_22_doc_string_vs_comments.main"
    assert meta["summary"].startswith("Convert a weight in grams")
    assert meta["signature"] == "(grams: 'float', ingredient: 'str') -> 'float'"
    assert meta["defaults"] is None


def test_audit_docstring():
    assert audit_docstring(grams_to_cups) == []
    assert audit_docstring(undocumented) == ["missing docstring"]
    assert audit_docstring(celsius_to_gas_mark) == [
        "parameters are not documented in an Args: section",
        "missing Returns: section",
    ]


def test_split_comments_and_docstrings():
    source = 'def f():\n    """Doc."""\n    x = "not a docstring"  # why\n    return x\n'
    assert split_comments_and_docstrings(source) == {"comments": ["why"], "docstrings": ["Doc."]}


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "grams_to_cups        audit: passes" in out
    assert "1 docstring, 2 comments" in out
