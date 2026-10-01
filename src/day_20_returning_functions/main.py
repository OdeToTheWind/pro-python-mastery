"""Day 20 – Returning Functions.

Scenario: a *blog post analyser* – functions that return values, multiple
values, exit early on bad input, return other functions and compose into a
text-processing pipeline.

Deliverables (syllabus):
* ``return`` statements
* Returning multiple values
* Early returns (guard clauses)
* Function composition
"""

from __future__ import annotations

import re
from collections.abc import Callable
from functools import reduce

DELIVERABLES: dict[str, str] = {
    "return statement": "reading_time",
    "returning multiple values (tuple unpacking)": "text_stats",
    "early returns / guard clauses": "validate_title",
    "functions that return functions": "make_truncator",
    "function composition": "compose",
}

WORDS_PER_MINUTE = 200


def reading_time(word_count: int) -> int:
    """Minutes to read, rounded up (``-(-a // b)`` is ceiling division)."""
    if word_count < 0:
        raise ValueError("word_count cannot be negative")
    return -(-word_count // WORDS_PER_MINUTE)


def text_stats(text: str) -> tuple[int, int, float]:
    """Return *three* values at once: word count, sentence count, average word length."""
    words = re.findall(r"[A-Za-z']+", text)
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    if not words:
        return 0, len(sentences), 0.0
    return len(words), len(sentences), round(sum(map(len, words)) / len(words), 2)


def validate_title(title: str) -> tuple[bool, str]:
    """Guard clauses: each check returns immediately, so no deep ``if`` nesting."""
    if not title.strip():
        return False, "title is empty"
    if len(title) > 70:
        return False, "title longer than 70 characters"
    if title != title.strip():
        return False, "title has leading or trailing spaces"
    if not title[0].isupper():
        return False, "title should start with a capital letter"
    return True, "ok"


def make_truncator(limit: int, suffix: str = "…") -> Callable[[str], str]:
    """Return a *new function* that remembers ``limit`` (a closure)."""
    if limit <= len(suffix):
        raise ValueError("limit must be longer than the suffix")

    def truncate(text: str) -> str:
        return text if len(text) <= limit else text[: limit - len(suffix)].rstrip() + suffix

    return truncate


def compose(*functions: Callable[[str], str]) -> Callable[[str], str]:
    """``compose(f, g, h)(x) == h(g(f(x)))`` – left-to-right pipeline."""

    def pipeline(value: str) -> str:
        return reduce(lambda acc, func: func(acc), functions, value)

    return pipeline


def collapse_spaces(text: str) -> str:
    return " ".join(text.split())


def strip_markdown(text: str) -> str:
    return re.sub(r"[*_`#>]", "", text)


make_excerpt = compose(strip_markdown, collapse_spaces, make_truncator(40))


def main() -> None:
    post = "# Why *Python*?\n\nPython reads like English.   It is fun! Isn't it?"
    words, sentences, avg = text_stats(post)  # unpacking multiple return values
    print("Day 20 – Blog analyser\n")
    print(f"words={words} sentences={sentences} avg_len={avg} read={reading_time(words)} min")
    for title in ["why python", "Why Python?", " Padded ", "X" * 80]:
        print(f"  {title[:20]!r:<24} → {validate_title(title)}")
    print("Excerpt:", make_excerpt(post))


if __name__ == "__main__":
    main()
