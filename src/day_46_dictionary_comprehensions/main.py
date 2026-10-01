"""Day 46 – Dictionary Comprehensions.

Scenario: an *online bookshop catalogue* – index products, reprice them,
invert lookups and count words in reviews, each with a dict comprehension.

Deliverables (syllabus):
* Efficient dictionary creation
* Dictionary transformation (filter, remap keys/values, invert, merge, nest)
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

DELIVERABLES: dict[str, str] = {
    "creation from a list of records": "index_by",
    "creation from two sequences (zip)": "price_list",
    "transformation of values": "apply_discount",
    "filtering by value": "filter_items",
    "inverting a mapping safely": "invert",
    "nested dict comprehension": "stock_matrix",
    "counting with a comprehension": "word_frequencies",
}

CATALOGUE: list[dict[str, Any]] = [
    {"isbn": "111", "title": "Fluent Python", "genre": "tech", "price": Decimal("49.90"), "stock": 4},
    {"isbn": "222", "title": "Dune", "genre": "sci-fi", "price": Decimal("12.50"), "stock": 0},
    {"isbn": "333", "title": "Clean Code", "genre": "tech", "price": Decimal("38.00"), "stock": 7},
    {"isbn": "444", "title": "Emma", "genre": "classic", "price": Decimal("8.99"), "stock": 2},
]


def index_by(records: Iterable[dict[str, Any]], key: str) -> dict[Any, dict[str, Any]]:
    """``{record[key]: record}`` – O(1) lookups instead of scanning a list."""
    index = {record[key]: record for record in records}
    return index


def price_list(titles: list[str], prices: list[Decimal]) -> dict[str, Decimal]:
    return {title: price for title, price in zip(titles, prices, strict=True)}


def apply_discount(prices: dict[str, Decimal], percent: int) -> dict[str, Decimal]:
    """Transform every value; keys stay the same."""
    if not 0 <= percent <= 100:
        raise ValueError("percent must be 0–100")
    factor = Decimal(100 - percent) / 100
    return {k: (v * factor).quantize(Decimal("0.01"), ROUND_HALF_UP) for k, v in prices.items()}


def filter_items[K, V](mapping: dict[K, V], predicate: Callable[[V], bool]) -> dict[K, V]:
    return {k: v for k, v in mapping.items() if predicate(v)}


def invert[K, V](mapping: dict[K, V]) -> dict[V, list[K]]:
    """Swap keys and values. Values may repeat, so each maps to a *list* of keys."""
    values = list(dict.fromkeys(mapping.values()))  # unique, in first-seen order
    return {v: [k for k, value in mapping.items() if value == v] for v in values}


def stock_matrix(records: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Nested comprehension: genre → {title: stock}."""
    genres = sorted({r["genre"] for r in records})  # a *set* comprehension
    return {g: {r["title"]: r["stock"] for r in records if r["genre"] == g} for g in genres}


def word_frequencies(text: str, min_length: int = 3) -> dict[str, int]:
    words = [w for w in re.findall(r"[a-z']+", text.lower()) if len(w) >= min_length]
    counts = {w: words.count(w) for w in set(words)}
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def merge_prices(*sources: dict[str, Decimal]) -> dict[str, Decimal]:
    """Later sources win – the same as ``{**a, **b}`` but for any number of dicts."""
    return {k: v for source in sources for k, v in source.items()}


def main() -> None:
    print("Day 46 – Bookshop catalogue\n")
    by_isbn = index_by(CATALOGUE, "isbn")
    print("lookup 333 →", by_isbn["333"]["title"])
    prices = {r["title"]: r["price"] for r in CATALOGUE}
    print("sale (20 % off):", apply_discount(prices, 20))
    in_stock = filter_items({r["title"]: r["stock"] for r in CATALOGUE}, lambda n: n > 0)
    print("in stock:", in_stock)
    print("titles by genre:", invert({r["title"]: r["genre"] for r in CATALOGUE}))
    print("stock matrix:", stock_matrix(CATALOGUE))
    print("review words:", word_frequencies("Great book. Great pace, great characters – a must read book!"))


if __name__ == "__main__":
    main()
