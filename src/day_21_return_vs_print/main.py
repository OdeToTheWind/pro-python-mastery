"""Day 21 – Return vs. Print.

Scenario: a *freelancer invoicing tool* – the same calculations written two
ways (print-only vs return) to show why returning data is the reusable design.

Deliverables (syllabus):
* Differentiating output (``print``) from return values
* Reusability
* Function design: pure core, thin I/O shell
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

DELIVERABLES: dict[str, str] = {
    "print-only function (anti-pattern)": "print_line_total",
    "returning function (reusable)": "line_total",
    "return value of a print-only function is None": "compare_designs",
    "reusability: composing returned values": "invoice_totals",
    "function design: pure core + I/O shell": "render_invoice",
}

CENT = Decimal("0.01")


@dataclass(frozen=True, slots=True)
class Line:
    description: str
    hours: Decimal
    rate: Decimal


def print_line_total(line: Line) -> None:
    """Anti-pattern: the result is shown but lost – callers get ``None``."""
    print(f"{line.description}: {(line.hours * line.rate).quantize(CENT)}")


def line_total(line: Line) -> Decimal:
    """Reusable: returns the amount so callers can add, test or format it."""
    if line.hours < 0 or line.rate < 0:
        raise ValueError("hours and rate must be non-negative")
    return (line.hours * line.rate).quantize(CENT, rounding=ROUND_HALF_UP)


def invoice_totals(lines: list[Line], tax_rate: Decimal, discount: Decimal = Decimal("0")) -> dict[str, Decimal]:
    """Built entirely from returned values – impossible with the print-only version."""
    if not Decimal("0") <= discount <= Decimal("1"):
        raise ValueError("discount must be between 0 and 1")
    subtotal = sum((line_total(line) for line in lines), Decimal("0"))
    discounted = (subtotal * (1 - discount)).quantize(CENT, rounding=ROUND_HALF_UP)
    tax = (discounted * tax_rate).quantize(CENT, rounding=ROUND_HALF_UP)
    return {"subtotal": subtotal, "discounted": discounted, "tax": tax, "total": discounted + tax}


def render_invoice(client: str, lines: list[Line], tax_rate: Decimal) -> str:
    """Return the formatted text; the caller decides whether to print, email or save it."""
    totals = invoice_totals(lines, tax_rate)
    rows = [f"INVOICE – {client}", "-" * 40]
    rows += [f"{line.description:<26}{line_total(line):>14}" for line in lines]
    rows += ["-" * 40] + [f"{key.title():<26}{value:>14}" for key, value in totals.items()]
    return "\n".join(rows)


def compare_designs(line: Line) -> tuple[object, Decimal]:
    """Capture what each design gives back to its caller."""
    from_print = print_line_total(line)  # type: ignore[func-returns-value]
    from_return = line_total(line)
    return from_print, from_return


def show(text: str, output: Callable[[str], None] = print) -> None:
    """The thin I/O shell: the only place that prints."""
    output(text)


def main() -> None:
    lines = [Line("Website design", Decimal("12"), Decimal("45")),
             Line("Bug fixes", Decimal("3.5"), Decimal("60"))]
    print("Day 21 – Return vs print\n")
    printed, returned = compare_designs(lines[0])
    print(f"print-only gave the caller: {printed!r}; return gave: {returned!r}\n")
    show(render_invoice("Acme Ltd", lines, Decimal("0.18")))


if __name__ == "__main__":
    main()
