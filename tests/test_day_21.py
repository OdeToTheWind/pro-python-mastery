"""Tests for Day 21 – Return vs. Print."""

from decimal import Decimal

import pytest

from src.day_21_return_vs_print.main import (
    Line,
    compare_designs,
    invoice_totals,
    line_total,
    main,
    print_line_total,
    render_invoice,
    show,
)

DESIGN = Line("Design", Decimal("12"), Decimal("45"))
FIXES = Line("Fixes", Decimal("3.5"), Decimal("60"))


def test_print_only_returns_none_but_prints(capsys):
    assert print_line_total(DESIGN) is None
    assert capsys.readouterr().out == "Design: 540.00\n"


def test_line_total_returns_value_without_printing(capsys):
    assert line_total(FIXES) == Decimal("210.00")
    assert capsys.readouterr().out == ""


def test_line_total_validation():
    with pytest.raises(ValueError):
        line_total(Line("x", Decimal("-1"), Decimal("10")))


def test_compare_designs():
    printed, returned = compare_designs(DESIGN)
    assert printed is None and returned == Decimal("540.00")


def test_invoice_totals_reuse_returned_values():
    totals = invoice_totals([DESIGN, FIXES], Decimal("0.18"), discount=Decimal("0.10"))
    assert totals == {
        "subtotal": Decimal("750.00"),
        "discounted": Decimal("675.00"),
        "tax": Decimal("121.50"),
        "total": Decimal("796.50"),
    }


@pytest.mark.parametrize("discount", ["-0.1", "1.5"])
def test_invoice_discount_range(discount):
    with pytest.raises(ValueError):
        invoice_totals([DESIGN], Decimal("0.18"), Decimal(discount))


def test_render_invoice_returns_text(capsys):
    text = render_invoice("Acme", [DESIGN], Decimal("0.2"))
    assert capsys.readouterr().out == ""
    assert text.splitlines()[0] == "INVOICE – Acme"
    assert text.splitlines()[-1].endswith("648.00")


def test_show_uses_injected_output():
    captured: list[str] = []
    show("hello", captured.append)
    assert captured == ["hello"]


def test_main(capsys):
    main()
    assert "print-only gave the caller: None" in capsys.readouterr().out
