"""Day 04 – Variable Naming Rules.

Scenario: a *code-review bot* that inspects proposed variable names and gives
the author syntax errors (must fix) and PEP 8 style warnings (should fix).

Deliverables (syllabus):
* PEP 8 naming conventions (snake_case, CONSTANT_CASE, CapWords)
* Reserved keywords (hard and soft)
* Descriptive names and constants
"""

from __future__ import annotations

import builtins
import keyword
import re
from collections.abc import Callable
from dataclasses import dataclass, field

DELIVERABLES: dict[str, str] = {
    "identifier syntax rules": "review_name",
    "reserved (hard) keywords": "review_name",
    "soft keywords (match, case, type, _)": "review_name",
    "PEP 8 style classification": "classify_style",
    "descriptive names": "review_name",
    "constants": "MAX_LOGIN_ATTEMPTS",
    "camelCase → snake_case refactor": "to_snake_case",
}

# Constants: module-level, ALL_CAPS, never reassigned by convention.
MAX_LOGIN_ATTEMPTS = 3
AMBIGUOUS_NAMES = frozenset({"l", "O", "I"})
MIN_DESCRIPTIVE_LENGTH = 3
ALLOWED_SHORT_NAMES = frozenset({"i", "j", "k", "x", "y", "z", "n", "_"})

_SNAKE = re.compile(r"_?[a-z][a-z0-9]*(?:_[a-z0-9]+)*_?")
_CONSTANT = re.compile(r"_?[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*")
_CAPWORDS = re.compile(r"_?(?:[A-Z][a-z0-9]+)+")


@dataclass(slots=True)
class NameReview:
    name: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors


def classify_style(name: str) -> str:
    """Return ``snake_case``, ``CONSTANT_CASE``, ``CapWords`` or ``mixed``."""
    if _SNAKE.fullmatch(name):
        return "snake_case"
    if _CONSTANT.fullmatch(name):
        return "CONSTANT_CASE"
    if _CAPWORDS.fullmatch(name):
        return "CapWords"
    return "mixed"


def to_snake_case(name: str) -> str:
    """Convert ``camelCase``/``CapWords``/``kebab-case`` to ``snake_case``."""
    name = name.replace("-", "_").replace(" ", "_")
    name = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name)
    name = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", name)
    return re.sub(r"_+", "_", name).lower()


def review_name(name: str, *, kind: str = "variable") -> NameReview:
    """Review *name* used as a ``variable``, ``constant`` or ``class``."""
    review = NameReview(name)
    if not name.isidentifier():
        # isidentifier() implements the real lexer rules, including Unicode:
        # "x²" fails because "²" is a digit-like symbol, not a letter.
        review.errors.append("not a valid Python identifier")
        return review
    if keyword.iskeyword(name):
        review.errors.append("reserved keyword – cannot be assigned")
        return review

    if keyword.issoftkeyword(name):
        review.warnings.append("soft keyword – legal, but confusing in match/type statements")
    if name in dir(builtins):
        review.warnings.append(f"shadows the built-in {name}()")
    if name in AMBIGUOUS_NAMES:
        review.warnings.append("looks like the digits 1 or 0 (PEP 8 forbids l, O, I)")
    elif len(name.strip("_")) < MIN_DESCRIPTIVE_LENGTH and name not in ALLOWED_SHORT_NAMES:
        review.warnings.append("too short to be descriptive")

    expected = {"variable": "snake_case", "constant": "CONSTANT_CASE", "class": "CapWords"}[kind]
    style = classify_style(name)
    if style != expected and name not in AMBIGUOUS_NAMES:
        hint = f" (try {to_snake_case(name)!r})" if expected == "snake_case" else ""
        review.warnings.append(f"PEP 8 expects {expected} for a {kind}, got {style}{hint}")
    return review


def format_review(review: NameReview) -> str:
    mark = "✅" if review.is_valid and not review.warnings else ("⚠️ " if review.is_valid else "❌")
    notes = "; ".join(review.errors + review.warnings) or "looks great"
    return f"{mark} {review.name:<16} {notes}"


def main(ask: Callable[[str], str] | None = None) -> None:
    ask = ask or input  # resolved at call time so tests can patch input()
    print("Day 04 – Variable naming review bot\n")
    samples = ["user_age", "totalPrice", "2fast", "class", "match", "max", "l", "x²", "_cache", "id"]
    for sample in samples:
        print(format_review(review_name(sample)))
    print(format_review(review_name("MAX_LOGIN_ATTEMPTS", kind="constant")))
    print(format_review(review_name("HttpClient", kind="class")))
    print(f"\nConstant in use: MAX_LOGIN_ATTEMPTS = {MAX_LOGIN_ATTEMPTS}")
    print("\nTry your own names (blank line or Ctrl-D to finish):")
    while True:
        try:
            name = ask("name → ").strip()
        except EOFError:
            break
        if not name:
            break
        print(format_review(review_name(name)))


if __name__ == "__main__":
    main()
