"""Day 05 – Mathematical Operations.

Scenario: a *restaurant bill splitter* – arithmetic with money, where rounding,
floor division and division by zero all matter.

Deliverables (syllabus):
* Arithmetic operators ``+ - * / // % **``
* Operator precedence
* Floor division (including negative numbers)
* Safe division handling
"""

from __future__ import annotations

import operator
from collections.abc import Callable
from decimal import ROUND_HALF_UP, Decimal

DELIVERABLES: dict[str, str] = {
    "arithmetic operators": "calculate",
    "operator precedence": "precedence_examples",
    "floor division and modulo with negatives": "floor_division_facts",
    "safe division": "safe_divide",
    "practical application (bill splitting)": "split_bill",
}

OPERATORS: dict[str, Callable[[float, float], float]] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
    "**": operator.pow,
}
MAX_EXPONENT = 1_000


def calculate(a: float, op: str, b: float) -> float:
    """Apply a binary operator. Raises instead of returning error strings.

    * ``ValueError`` for an unknown operator or a huge exponent
    * ``ZeroDivisionError`` for ``/``, ``//`` or ``%`` by zero
    * ``OverflowError`` if a float result is too large
    """
    try:
        func = OPERATORS[op]
    except KeyError:
        raise ValueError(f"unknown operator {op!r}") from None
    if op == "**" and abs(b) > MAX_EXPONENT:
        raise ValueError(f"exponent larger than {MAX_EXPONENT} is not allowed")
    result = func(a, b)
    if isinstance(result, complex):
        raise ValueError("result is a complex number (negative base, fractional exponent)")
    return result


def safe_divide(a: float, b: float, default: float | None = None) -> float | None:
    """Divide, returning *default* instead of raising on division by zero."""
    try:
        return a / b
    except ZeroDivisionError:
        return default


def floor_division_facts(a: int, b: int) -> dict[str, int | float | bool]:
    """Show that ``//`` rounds towards −∞ and that ``a == b*(a//b) + a%b`` always holds."""
    quotient, remainder = divmod(a, b)
    return {
        "a // b": quotient,
        "a % b": remainder,
        "a / b": a / b,
        "int(a / b)": int(a / b),  # truncates toward zero – differs for negatives
        "identity holds": a == b * quotient + remainder,
    }


def precedence_examples() -> list[tuple[str, float]]:
    """Expressions whose value changes once you add parentheses."""
    return [
        ("2 + 3 * 4", 2 + 3 * 4),
        ("(2 + 3) * 4", (2 + 3) * 4),
        ("-2 ** 2", -(2**2)),  # ** binds tighter than unary minus
        ("(-2) ** 2", (-2) ** 2),
        ("2 ** 3 ** 2", 2 ** (3**2)),  # ** is right-associative
        ("(2 ** 3) ** 2", (2**3) ** 2),
        ("10 - 4 - 3", 10 - 4 - 3),  # - is left-associative
        ("10 / 4 * 2", 10 / 4 * 2),
    ]


def split_bill(total: str, people: int, tip_percent: int = 0) -> list[Decimal]:
    """Split a bill fairly, distributing leftover cents to the first payers.

    Uses ``Decimal`` (exact money) plus ``divmod`` on integer cents so the
    shares always add back up to the total – floats would not.
    """
    if people <= 0:
        raise ValueError("at least one person must pay")
    amount = Decimal(total) * (100 + tip_percent) / 100
    cents = int(amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) * 100)
    share, leftover = divmod(cents, people)
    return [Decimal(share + (1 if i < leftover else 0)) / 100 for i in range(people)]


def main(ask: Callable[[str], str] | None = None) -> None:
    ask = ask or input  # resolved at call time so tests can patch input()
    print("Day 05 – Mathematical Operations\n")
    print("Precedence:")
    for expr, value in precedence_examples():
        print(f"  {expr:<15} = {value}")
    print("\nFloor division with negatives (-7, 2):")
    for key, value in floor_division_facts(-7, 2).items():
        print(f"  {key:<15} = {value}")
    print(f"\nSafe divide 10 / 0 → {safe_divide(10, 0, default=float('inf'))}")
    shares = split_bill("100.00", 3, tip_percent=10)
    print(f"Split €100 + 10% tip between 3: {[str(s) for s in shares]} (sum {sum(shares)})")

    print("\nCalculator – enter 'a op b' (e.g. 7 // 2), blank to quit:")
    while True:
        try:
            line = ask("calc → ").strip()
        except EOFError:
            break
        if not line:
            break
        try:
            a_text, op, b_text = line.split()
            print(f"  = {calculate(float(a_text), op, float(b_text))}")
        except (ValueError, ZeroDivisionError, OverflowError) as exc:
            print(f"  ✗ {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
