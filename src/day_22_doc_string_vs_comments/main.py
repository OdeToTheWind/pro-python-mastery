"""Day 22 – Docstrings vs. Comments.

Scenario: a *kitchen unit-conversion library* that is documented properly and
a documentation auditor that inspects it.

Deliverables (syllabus):
* ``#`` comments vs ``\"\"\"`` docstrings
* Documentation standards (PEP 257, Google style)
* Function metadata (``__doc__``, ``__name__``, ``__annotations__``, signature …)
"""

from __future__ import annotations

import inspect
import io
import tokenize
from collections.abc import Callable
from typing import Any

DELIVERABLES: dict[str, str] = {
    "docstrings (PEP 257, Google style)": "grams_to_cups",
    "comments vs docstrings at runtime": "split_comments_and_docstrings",
    "documentation standards check": "audit_docstring",
    "function metadata": "function_metadata",
}

GRAMS_PER_CUP = {"flour": 120.0, "sugar": 200.0, "butter": 227.0}


def grams_to_cups(grams: float, ingredient: str) -> float:
    """Convert a weight in grams to US cups for a baking ingredient.

    Args:
        grams: Weight in grams. Must not be negative.
        ingredient: One of ``flour``, ``sugar`` or ``butter``.

    Returns:
        The volume in cups, rounded to two decimals.

    Raises:
        ValueError: If *grams* is negative or the ingredient is unknown.

    Example:
        >>> grams_to_cups(240, "flour")
        2.0
    """
    # Comments explain *why* to maintainers and are discarded by the compiler:
    # densities differ a lot, so a single "grams per cup" constant would be wrong.
    if grams < 0:
        raise ValueError("grams must not be negative")
    try:
        density = GRAMS_PER_CUP[ingredient]
    except KeyError:
        raise ValueError(f"unknown ingredient {ingredient!r}") from None
    return round(grams / density, 2)


def celsius_to_gas_mark(celsius: float) -> int:
    """Return the nearest UK gas mark (1–9) for an oven temperature in °C."""
    return max(1, min(9, round((celsius - 121) / 14)))


def undocumented(x):  # type: ignore[no-untyped-def]
    # A comment is not documentation: help() and IDEs cannot see it.
    return x


def function_metadata(func: Callable[..., Any]) -> dict[str, Any]:
    """Collect the metadata Python stores on every function object."""
    doc = inspect.getdoc(func)  # dedented, unlike raw __doc__
    return {
        "name": func.__name__,
        "qualname": func.__qualname__,
        "module": func.__module__,
        "summary": doc.splitlines()[0] if doc else None,
        "signature": str(inspect.signature(func)),
        "annotations": inspect.get_annotations(func),
        "defaults": func.__defaults__,
    }


def audit_docstring(func: Callable[..., Any]) -> list[str]:
    """Check a docstring against PEP 257 and Google-style sections."""
    doc = inspect.getdoc(func)
    if not doc:
        return ["missing docstring"]
    problems: list[str] = []
    summary = doc.splitlines()[0]
    if not summary.endswith("."):
        problems.append("summary line should end with a period")
    params = [p for p in inspect.signature(func).parameters if p not in {"self", "cls"}]
    if params and "Args:" not in doc:
        problems.append("parameters are not documented in an Args: section")
    if "Returns:" not in doc and inspect.signature(func).return_annotation not in (None, "None"):
        problems.append("missing Returns: section")
    return problems


def split_comments_and_docstrings(source: str) -> dict[str, list[str]]:
    """Use the tokenizer to separate ``#`` comments from docstring literals."""
    comments, docstrings = [], []
    previous_significant = tokenize.NEWLINE
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type == tokenize.COMMENT:
            comments.append(token.string.lstrip("# ").rstrip())
        elif token.type == tokenize.STRING and previous_significant in (tokenize.INDENT, tokenize.NEWLINE):
            docstrings.append(token.string.strip("\"'").strip())
        if token.type not in (tokenize.COMMENT, tokenize.NL):
            previous_significant = token.type
    return {"comments": comments, "docstrings": docstrings}


def main() -> None:
    print("Day 22 – Documentation auditor\n")
    print("grams_to_cups(240, 'flour') =", grams_to_cups(240, "flour"))
    for func in (grams_to_cups, celsius_to_gas_mark, undocumented):
        print(f"{func.__name__:<20} audit: {audit_docstring(func) or 'passes'}")
    meta = function_metadata(grams_to_cups)
    print("\nMetadata:", {k: meta[k] for k in ("name", "summary", "signature")})
    source = inspect.getsource(grams_to_cups)
    split = split_comments_and_docstrings(source)
    print(f"Tokens: {len(split['docstrings'])} docstring, {len(split['comments'])} comments")


if __name__ == "__main__":
    main()
