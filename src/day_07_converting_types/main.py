"""Day 07 – Converting Types (Casting).

Scenario: a *spreadsheet import cleaner* – every cell arrives as text and must
be cast to the right Python type, with precise error reporting.

Deliverables (syllabus):
* ``int() float() str() bool() list() tuple() set() dict()``
* ``ValueError`` (right type, bad content) vs ``TypeError`` (wrong type)
"""

from __future__ import annotations

import ast
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

DELIVERABLES: dict[str, str] = {
    "int/float/str/bool casts": "convert",
    "list/tuple/set/dict casts": "convert",
    "parsing collections from text": "parse_collection",
    "bool('False') pitfall and strict parsing": "parse_bool",
    "ValueError vs TypeError": "error_examples",
}

TRUE_WORDS = frozenset({"true", "yes", "y", "1", "on"})
FALSE_WORDS = frozenset({"false", "no", "n", "0", "off", ""})

CASTS: dict[str, Callable[[Any], Any]] = {
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
    "list": list,
    "tuple": tuple,
    "set": set,
    "dict": dict,
}


@dataclass(frozen=True, slots=True)
class Conversion:
    ok: bool
    value: Any = None
    error_type: str | None = None
    message: str = ""


def parse_bool(text: str) -> bool:
    """Strictly parse yes/no words. ``bool("False")`` would be ``True``!"""
    word = text.strip().lower()
    if word in TRUE_WORDS:
        return True
    if word in FALSE_WORDS:
        return False
    raise ValueError(f"{text!r} is not a recognised boolean word")


def parse_collection(text: str, target: str) -> Any:
    """Turn ``"[1, 2]"`` / ``"{'a': 1}"`` into real objects, then cast to *target*."""
    literal = ast.literal_eval(text)
    return CASTS[target](literal)


def convert(value: Any, target: str) -> Conversion:
    """Cast *value* to *target* and report exactly which error happened."""
    if target not in CASTS:
        return Conversion(False, error_type="KeyError", message=f"unknown target {target!r}")
    try:
        if isinstance(value, str) and target == "bool":
            result = parse_bool(value)
        elif isinstance(value, str) and target in {"list", "tuple", "set", "dict"} and value[:1] in "[({":
            result = parse_collection(value, target)
        else:
            result = CASTS[target](value)
    except (ValueError, SyntaxError) as exc:
        return Conversion(False, error_type=type(exc).__name__, message=str(exc))
    except TypeError as exc:
        return Conversion(False, error_type="TypeError", message=str(exc))
    except OverflowError as exc:  # int(float("inf"))
        return Conversion(False, error_type="OverflowError", message=str(exc))
    return Conversion(True, value=result)


def error_examples() -> dict[str, str]:
    """Which casts raise which exception, and why."""
    cases: dict[str, Callable[[], object]] = {
        "int('12.5')": lambda: int("12.5"),
        "int('abc')": lambda: int("abc"),
        "int([1, 2])": lambda: int([1, 2]),  # type: ignore[call-overload]
        "float(None)": lambda: float(None),  # type: ignore[arg-type]
        "dict([1, 2])": lambda: dict([1, 2]),  # type: ignore[arg-type]
        "dict(['ab', 'cd'])": lambda: dict(["ab", "cd"]),  # type: ignore[arg-type]
        "int(float('inf'))": lambda: int(float("inf")),
        "list(42)": lambda: list(42),  # type: ignore[call-overload]
    }
    outcome: dict[str, str] = {}
    for label, func in cases.items():
        try:
            outcome[label] = f"ok → {func()!r}"
        except Exception as exc:  # noqa: BLE001 – we want to show every class
            outcome[label] = type(exc).__name__
    return outcome


def main() -> None:
    print("Day 07 – Converting Types\n")
    cells = [("42", "int"), ("12.5", "int"), ("12.5", "float"), ("False", "bool"),
             ("maybe", "bool"), ("[1, 2, 2]", "set"), ("[('a', 1)]", "dict"), (3, "list")]
    for value, target in cells:
        result = convert(value, target)
        shown = repr(result.value) if result.ok else f"{result.error_type}: {result.message}"
        print(f"{value!r:>14} → {target:<5} {shown}")
    print(f"\nPitfall: bool('False') is {bool('False')}, parse_bool('False') is {parse_bool('False')}")
    print("\nValueError vs TypeError:")
    for label, outcome in error_examples().items():
        print(f"  {label:<20} {outcome}")


if __name__ == "__main__":
    main()
