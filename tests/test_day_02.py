"""Tests for Day 02 – String Manipulation."""

import pytest

from src.day_02_strings.main import (
    BADGE_WIDTH,
    align_columns,
    clean_name,
    main,
    make_handle,
    render_badge,
    slugify,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("  ada   LOVELACE ", "Ada Lovelace"),
        ("john's", "John's"),  # str.title() would give "John'S"
        ("mary-jane o'neil", "Mary-Jane O'neil"),
        ("\tgrace\nhopper", "Grace Hopper"),
    ],
)
def test_clean_name(raw, expected):
    assert clean_name(raw) == expected


def test_clean_name_rejects_blank():
    with pytest.raises(ValueError):
        clean_name("   ")


@pytest.mark.parametrize(
    ("name", "years", "expected"),
    [("Ada Lovelace", 5, "@ada05"), ("Al", 0, "@al00"), ("O'Neil", 12, "@one12")],
)
def test_make_handle(name, years, expected):
    assert make_handle(name, years) == expected


@pytest.mark.parametrize(("name", "years"), [("Ada", -1), ("1234", 3)])
def test_make_handle_rejects_bad_input(name, years):
    with pytest.raises(ValueError):
        make_handle(name, years)


def test_slugify():
    assert slugify("  Hello, World!  ") == "hello-world"
    assert slugify("***") == ""


def test_render_badge_lines_are_fixed_width_and_centred():
    lines = render_badge("ada lovelace", "dev", 8).splitlines()
    assert all(len(line) == BADGE_WIDTH for line in lines)
    assert lines[3].strip() == "Ada Lovelace"
    assert lines[4].strip() == "DEV"
    assert lines[5].strip(".") == "@ada08"


def test_align_columns():
    (line,) = align_columns([("Ada", "Rome", 5)])
    assert line == "Ada" + " " * 12 + "   Rome   " + "    5.00"


def test_main(capsys):
    main()
    assert "Mary-Jane O'neil" in capsys.readouterr().out
