"""Tests for Day 64 – Iterators & the Iterator Protocol."""

from collections.abc import Iterable, Iterator

import pytest

from src.day_64_iterators_iterator_protocol.main import (
    MUSEUM,
    Collection,
    Countdown,
    PageCursor,
    first_match,
    main,
    manual_for_loop,
    read_until_sentinel,
)

ALL = ["Mona Lisa", "Starry Night", "The Scream", "Girl with a Pearl Earring"]


def test_cursor_implements_the_protocol():
    cursor = iter(MUSEUM)
    assert isinstance(cursor, Iterator)
    assert iter(cursor) is cursor
    assert next(cursor) == "Mona Lisa"


def test_cursor_skips_empty_pages_and_stops():
    cursor = iter(MUSEUM)
    assert list(cursor) == ALL
    assert cursor.pages_fetched == 4
    with pytest.raises(StopIteration):
        next(cursor)
    assert list(cursor) == []  # an iterator is one-pass


def test_cursor_is_lazy():
    calls = []

    def fetch(page):
        calls.append(page)
        return [f"item{page}"], page + 1 if page < 100 else None

    cursor = PageCursor(fetch)
    assert next(cursor) == "item1"
    assert calls == [1]  # only the pages actually needed are fetched


def test_collection_is_reiterable():
    assert isinstance(MUSEUM, Iterable) and not isinstance(MUSEUM, Iterator)
    assert list(MUSEUM) == list(MUSEUM) == ALL
    assert iter(MUSEUM) is not iter(MUSEUM)


def test_iterating_does_not_mutate_source_pages():
    pages = {1: (["a", "b"], None)}
    collection = Collection(pages)
    assert list(collection) == ["a", "b"]
    assert pages[1][0] == ["a", "b"]  # the cursor works on its own copy


def test_empty_collection():
    assert list(Collection({1: ([], None)})) == []


def test_countdown():
    assert list(Countdown(3)) == [3, 2, 1]
    assert list(Countdown(0)) == []
    with pytest.raises(ValueError):
        Countdown(-1)


def test_manual_for_loop_matches_for_statement():
    assert manual_for_loop(MUSEUM) == [item for item in MUSEUM]
    assert manual_for_loop("ab") == ["a", "b"]


def test_read_until_sentinel():
    assert read_until_sentinel(iter(["a", "b", "", "c"])) == ["a", "b"]
    assert read_until_sentinel(iter(["a"])) == ["a"]


def test_first_match_with_default():
    assert first_match(MUSEUM, "The") == "The Scream"
    assert first_match(MUSEUM, "Zzz") is None


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "pages fetched: 4" in out and "cursor reused (exhausted): []" in out
