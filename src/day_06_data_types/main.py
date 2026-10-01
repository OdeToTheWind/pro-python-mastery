"""Day 06 – Built-in Data Types.

Scenario: a *value inspector* – paste any Python literal and get a report on its
type, category, mutability, hashability and size.

Deliverables (syllabus):
* int, float, bool, str, list, tuple, dict, set
* Mutability (and aliasing consequences)
* Type checks with ``type()`` vs ``isinstance()``
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any

DELIVERABLES: dict[str, str] = {
    "core built-in types": "describe",
    "mutability": "describe",
    "aliasing consequences of mutability": "aliasing_demo",
    "type() vs isinstance()": "type_check_demo",
    "safe parsing of literals": "parse_literal",
}

CATEGORIES: dict[type, str] = {
    bool: "boolean",  # must come before int: bool is a subclass of int
    int: "numeric",
    float: "numeric",
    complex: "numeric",
    str: "text",
    bytes: "binary",
    list: "sequence",
    tuple: "sequence",
    range: "sequence",
    dict: "mapping",
    set: "set",
    frozenset: "set",
    type(None): "none",
}
MUTABLE_TYPES = (list, dict, set, bytearray)


@dataclass(frozen=True, slots=True)
class TypeReport:
    type_name: str
    category: str
    mutable: bool
    hashable: bool
    length: int | None


def is_hashable(value: object) -> bool:
    """A value is hashable only if ``hash()`` succeeds – ``([1],)`` is a tuple but not hashable."""
    try:
        hash(value)
    except TypeError:
        return False
    return True


def describe(value: object) -> TypeReport:
    category = next((name for kind, name in CATEGORIES.items() if type(value) is kind), "other")
    try:
        length: int | None = len(value)  # type: ignore[arg-type]
    except TypeError:
        length = None
    return TypeReport(
        type_name=type(value).__name__,
        category=category,
        mutable=isinstance(value, MUTABLE_TYPES),
        hashable=is_hashable(value),
        length=length,
    )


def parse_literal(text: str) -> Any:
    """Parse a literal safely; anything that is not a literal stays a string.

    ``ast.literal_eval`` never executes code, unlike ``eval``.
    """
    try:
        return ast.literal_eval(text.strip())
    except (ValueError, SyntaxError, MemoryError, RecursionError):
        return text


def aliasing_demo() -> dict[str, object]:
    """Two names, one list: mutating through one name is visible through the other."""
    original = [1, 2]
    alias = original
    copy = original.copy()
    alias.append(3)
    frozen = (1, 2)
    try:
        frozen[0] = 99  # type: ignore[index]
        tuple_mutated = True
    except TypeError:
        tuple_mutated = False
    return {
        "original": original,
        "copy": copy,
        "same object": alias is original,
        "tuple_mutated": tuple_mutated,
    }


def type_check_demo(value: object) -> dict[str, bool]:
    """``type(x) is int`` is exact; ``isinstance`` respects inheritance (``True`` is an int)."""
    return {
        "type is int": type(value) is int,
        "isinstance int": isinstance(value, int),
        "is real number": isinstance(value, int | float) and not isinstance(value, bool),
    }


def format_report(text: str) -> str:
    value = parse_literal(text)
    r = describe(value)
    return (
        f"{text!r:<22} → {r.type_name:<9} category={r.category:<8} "
        f"mutable={r.mutable!s:<5} hashable={r.hashable!s:<5} len={r.length}"
    )


def main() -> None:
    print("Day 06 – Built-in Data Types\n")
    for sample in ["42", "3.14", "True", "'hi'", "[1, 2]", "(1, [2])", "{'a': 1}", "{1, 2}",
                   "None", "hello world"]:
        print(format_report(sample))
    print("\nAliasing:", aliasing_demo())
    print("type() vs isinstance() for True:", type_check_demo(True))


if __name__ == "__main__":
    main()
