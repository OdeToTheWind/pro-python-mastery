"""Tests for Day 14 – Code Blocks and Indentation."""

import pytest

from src.day_14_code_block_indentation.main import (
    BROKEN_SNIPPETS,
    SAMPLE_PROGRAM,
    block_outline,
    check_snippet,
    fix_tabs,
    indent_body,
    main,
)


def test_valid_program_compiles():
    assert check_snippet(SAMPLE_PROGRAM).ok


@pytest.mark.parametrize(
    ("label", "error", "line", "message_part"),
    [
        ("expected an indented block", "IndentationError", 2, "expected an indented block"),
        ("unexpected indent", "IndentationError", 2, "unexpected indent"),
        ("unindent does not match", "IndentationError", 3, "unindent does not match"),
        ("mixed tabs and spaces", "TabError", 3, "inconsistent use of tabs"),
    ],
)
def test_broken_snippets_are_diagnosed(label, error, line, message_part):
    result = check_snippet(BROKEN_SNIPPETS[label])
    assert not result.ok
    assert (result.error, result.line) == (error, line)
    assert message_part in result.message


def test_other_syntax_errors_are_distinguished():
    assert check_snippet("if x == 1\n    pass\n").error == "SyntaxError"


def test_fix_tabs_repairs_tab_error():
    fixed = fix_tabs(BROKEN_SNIPPETS["mixed tabs and spaces"])
    assert "\t" not in fixed
    assert check_snippet(fixed).ok


def test_indent_body_repairs_missing_block():
    fixed = indent_body(BROKEN_SNIPPETS["expected an indented block"], after_line=1)
    assert fixed == "def greet():\n    print('hi')\n"
    assert check_snippet(fixed).ok


def test_block_outline_depths():
    assert block_outline(SAMPLE_PROGRAM) == [
        (0, "def count_evens(numbers):"),
        (1, "total = 0"),
        (1, "for n in numbers:"),
        (2, "if n % 2 == 0:"),
        (3, "total += 1"),
        (1, "return total"),
    ]


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "TabError on line 3" in out
    assert "tabs fixed   → True" in out
