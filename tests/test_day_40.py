"""Tests for Day 40 – Slicing."""

import pytest

from src.day_40_python_slice_function.main import (
    ACCOUNT,
    SAMPLE,
    chunk,
    describe_slice,
    drop_every_other,
    is_palindrome,
    main,
    mask_account,
    parse_record,
    replace_section,
    rotate,
    safe_slice,
)


def test_parse_record_with_named_slices():
    assert parse_record(SAMPLE[0]) == {
        "date": "2026-04-21",
        "account": "GB29NWBK60161331926819",
        "amount": -3.4,
        "memo": "COFFEE",
    }
    assert isinstance(ACCOUNT, slice)


def test_parse_record_too_short():
    with pytest.raises(ValueError):
        parse_record("2026-04-21")


@pytest.mark.parametrize(("visible", "expected"), [(4, "••••••6819"), (0, "••••••••••"), (20, "1331926819")])
def test_mask_account(visible, expected):
    assert mask_account("1331926819", visible) == expected


def test_palindrome_uses_reverse_slice():
    assert is_palindrome("Never odd or even")
    assert not is_palindrome("Python")


def test_safe_slice():
    assert safe_slice("abcdef", None, None, -2) == "fdb"
    assert safe_slice([1, 2, 3], 5, 10) == []
    with pytest.raises(ValueError):
        safe_slice("abc", 0, 3, 0)


@pytest.mark.parametrize(
    ("s", "length", "expected"),
    [(slice(None), 5, (0, 5, 1)), (slice(-3, None), 10, (7, 10, 1)), (slice(2, 100, 2), 6, (2, 6, 2)),
     (slice(None, None, -1), 4, (3, -1, -1))],
)
def test_describe_slice(s, length, expected):
    assert describe_slice(s, length) == expected


def test_replace_section_changes_length_without_mutating_input():
    original = [1, 2, 3, 4]
    assert replace_section(original, 1, 3, ["x"]) == [1, "x", 4]
    assert replace_section(original, 2, 2, ["a", "b"]) == [1, 2, "a", "b", 3, 4]
    assert original == [1, 2, 3, 4]


def test_drop_every_other():
    assert drop_every_other([0, 1, 2, 3, 4]) == [0, 2, 4]
    assert drop_every_other([]) == []


@pytest.mark.parametrize(("k", "expected"), [(1, [2, 3, 1]), (-1, [3, 1, 2]), (4, [2, 3, 1]), (0, [1, 2, 3])])
def test_rotate(k, expected):
    assert rotate([1, 2, 3], k) == expected


def test_rotate_empty():
    assert rotate([], 3) == []


def test_chunk():
    assert chunk("abcdefg", 3) == ["abc", "def", "g"]
    with pytest.raises(ValueError):
        chunk([1], 0)


def test_main(capsys):
    main()
    assert "••••••••••••••••••6819" in capsys.readouterr().out
