"""Day 49 – Strongly Dynamic Typing.

Scenario: a *product-import pipeline* receiving loosely typed data from
spreadsheets and APIs. Python is **dynamic** (names can be rebound to any type
at runtime) but **strong** (it refuses to silently mix incompatible types).

Deliverables (syllabus):
* Python's dynamic typing behaviour
* Python's strong typing behaviour (no implicit coercion)
* Practical implications: duck typing, explicit conversion, runtime checks,
  and type hints as documentation that tools – not the interpreter – enforce
"""

from __future__ import annotations

import functools
import inspect
from collections.abc import Callable
from typing import Any, get_type_hints

DELIVERABLES: dict[str, str] = {
    "dynamic typing (rebinding)": "rebinding_demo",
    "strong typing (no implicit coercion)": "strong_typing_errors",
    "explicit conversion": "add_quantities",
    "duck typing": "total_length",
    "hints are not enforced at runtime": "hints_not_enforced",
    "opt-in runtime enforcement": "enforce_types",
}


def rebinding_demo() -> list[str]:
    """One name, three types over time – the *object* has the type, not the name."""
    value: Any = 42
    seen = [type(value).__name__]
    value = "forty-two"
    seen.append(type(value).__name__)
    value = [4, 2]
    seen.append(type(value).__name__)
    return seen


def strong_typing_errors() -> dict[str, str]:
    """Operations JavaScript or PHP would coerce – Python raises ``TypeError``."""
    attempts: dict[str, Callable[[], object]] = {
        '"3" + 4': lambda: "3" + 4,  # type: ignore[operator]
        '[1] + (2,)': lambda: [1] + (2,),  # type: ignore[operator]
        '"5" * "2"': lambda: "5" * "2",  # type: ignore[operator]
        "None + 1": lambda: None + 1,  # type: ignore[operator]
        '"3" * 4': lambda: "3" * 4,  # allowed: repetition is a defined operation
        "True + 1": lambda: True + 1,  # allowed: bool is a subclass of int
    }
    results = {}
    for label, attempt in attempts.items():
        try:
            results[label] = repr(attempt())
        except TypeError:
            results[label] = "TypeError"
    return results


def add_quantities(a: object, b: object) -> int:
    """Explicit conversion at the boundary – the pipeline's answer to strong typing."""
    try:
        return int(str(a).strip()) + int(str(b).strip())
    except ValueError as exc:
        raise ValueError(f"cannot add {a!r} and {b!r} as quantities") from exc


def total_length(*items: object) -> int:
    """Duck typing: anything with ``len()`` counts; everything else counts as 1."""
    total = 0
    for item in items:
        try:
            total += len(item)  # type: ignore[arg-type]
        except TypeError:
            total += 1
    return total


def label_price(price: float) -> str:
    return f"€{price:.2f}"


def hints_not_enforced() -> str:
    """Type hints are documentation for humans and checkers like mypy, not runtime rules."""
    try:
        return label_price("9.99")  # type: ignore[arg-type]
    except (TypeError, ValueError) as exc:
        return f"{type(exc).__name__} raised by the f-string, not by the hint"


def enforce_types[F: Callable[..., Any]](func: F) -> F:
    """Decorator that checks simple (class) annotations at call time."""
    hints = get_type_hints(func)
    signature = inspect.signature(func)

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        bound = signature.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            expected = hints.get(name)
            if isinstance(expected, type) and not isinstance(value, expected):
                raise TypeError(f"{name} must be {expected.__name__}, got {type(value).__name__}")
        return func(*args, **kwargs)

    return wrapper  # type: ignore[return-value]


@enforce_types
def restock(sku: str, quantity: int) -> str:
    return f"{sku}: +{quantity}"


def main() -> None:
    print("Day 49 – Dynamic but strong typing\n")
    print("Rebinding one name:", rebinding_demo())
    for expr, outcome in strong_typing_errors().items():
        print(f"  {expr:<12} → {outcome}")
    print("Explicit conversion ' 3 ' + 4 →", add_quantities(" 3 ", 4))
    print("Duck typing total_length('abc', [1, 2], 7) →", total_length("abc", [1, 2], 7))
    print("Hint not enforced:", hints_not_enforced())
    print("Opt-in enforcement:", restock("SKU-1", 5))
    try:
        restock("SKU-1", "5")  # type: ignore[arg-type]
    except TypeError as exc:
        print("  rejected:", exc)


if __name__ == "__main__":
    main()
