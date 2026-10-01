"""Day 64 – Iterators & the Iterator Protocol.

Scenario: a *paginated API cursor for a museum collection* – the client hides
page requests behind a plain ``for`` loop, exactly like database cursors and
cloud SDK paginators do.

Deliverables (syllabus):
* ``__iter__`` and ``__next__`` (and ``StopIteration``)
* Custom iterators (stateful, one-pass)
* Iterables vs iterators (re-iterable containers that return fresh iterators)
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
from typing import Self

DELIVERABLES: dict[str, str] = {
    "__iter__ and __next__": "PageCursor",
    "StopIteration ends the loop": "PageCursor.__next__",
    "custom iterator with state": "Countdown",
    "iterable vs iterator (re-iterable container)": "Collection",
    "what a for loop really does": "manual_for_loop",
    "iter(callable, sentinel)": "read_until_sentinel",
    "next() with a default": "first_match",
}

Page = tuple[list[str], int | None]  # (items, next page number or None)


class PageCursor:
    """Yields every artwork across all pages, fetching pages lazily.

    It is an *iterator*: ``__iter__`` returns ``self`` and the cursor can be
    consumed only once – just like a file object or a database cursor.
    """

    def __init__(self, fetch_page: Callable[[int], Page], start_page: int = 1) -> None:
        self._fetch = fetch_page
        self._next_page: int | None = start_page
        self._buffer: list[str] = []
        self.pages_fetched = 0

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> str:
        while not self._buffer:
            if self._next_page is None:
                raise StopIteration  # the protocol's "no more items" signal
            items, self._next_page = self._fetch(self._next_page)
            # Copy! Popping from the fetched list itself would drain the source data
            # and break every later iteration of the collection.
            self._buffer = list(items)
            self.pages_fetched += 1
        return self._buffer.pop(0)


class Countdown:
    """A tiny stateful iterator: 3, 2, 1 then exhausted forever."""

    def __init__(self, start: int) -> None:
        if start < 0:
            raise ValueError("start must be non-negative")
        self.current = start

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1


@dataclass(frozen=True)
class Collection:
    """An *iterable*: each ``iter()`` call returns a brand-new cursor,
    so the collection can be looped over many times."""

    pages: dict[int, Page]

    def fetch(self, number: int) -> Page:
        return self.pages[number]

    def __iter__(self) -> PageCursor:
        return PageCursor(self.fetch)


def manual_for_loop[T](iterable: Iterable[T]) -> list[T]:
    """Exactly what ``for item in iterable:`` does behind the scenes."""
    seen = []
    iterator = iter(iterable)  # calls iterable.__iter__()
    while True:
        try:
            item = next(iterator)  # calls iterator.__next__()
        except StopIteration:
            break
        seen.append(item)
    return seen


def read_until_sentinel(chunks: Iterator[str], sentinel: str = "") -> list[str]:
    """``iter(callable, sentinel)`` keeps calling until the sentinel appears."""
    return list(iter(lambda: next(chunks, sentinel), sentinel))


def first_match(items: Iterable[str], prefix: str) -> str | None:
    """``next(generator, default)`` – no ``StopIteration`` when nothing matches."""
    return next((item for item in items if item.startswith(prefix)), None)


MUSEUM = Collection({
    1: (["Mona Lisa", "Starry Night"], 2),
    2: (["The Scream"], 3),
    3: ([], 4),  # APIs sometimes return an empty page before the last one
    4: (["Girl with a Pearl Earring"], None),
})


def main() -> None:
    print("Day 64 – Museum collection cursor\n")
    cursor = iter(MUSEUM)
    for number, title in enumerate(cursor, start=1):
        print(f"{number}. {title}")
    print(f"pages fetched: {cursor.pages_fetched}; second pass over the collection: {len(list(MUSEUM))} items")
    print("cursor reused (exhausted):", list(cursor))
    print("manual loop:", manual_for_loop(Countdown(3)))
    print("until blank chunk:", read_until_sentinel(iter(["GET", "/", "", "ignored"])))
    print("first 'The':", first_match(MUSEUM, "The"), "| first 'Z':", first_match(MUSEUM, "Z"))


if __name__ == "__main__":
    main()
