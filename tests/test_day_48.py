"""Tests for Day 48 – Tkinter GUI.

The calculation is tested everywhere. The widget tree is tested only where
Tkinter and a display are available (marked ``gui``).
"""

from decimal import Decimal

import pytest

from src.day_48_tkinter_gui.main import TipResult, calculate_tip


def test_basic_split():
    assert calculate_tip("86.40", 15, "3") == TipResult(Decimal("12.96"), Decimal("99.36"), Decimal("33.12"))


def test_comma_decimal_and_whitespace():
    assert calculate_tip(" 10,00 ", 10, "1").total == Decimal("11.00")


def test_round_up_adjusts_tip():
    result = calculate_tip("100", 10, "3", round_up=True)
    assert result.per_person == Decimal("37")
    assert result.total == Decimal("111") and result.tip == Decimal("11")


@pytest.mark.parametrize(
    ("bill", "percent", "people", "message"),
    [("abc", 10, "2", "number"), ("0", 10, "2", "greater than zero"), ("10", 31, "2", "between"),
     ("10", 10, "0", "People"), ("10", 10, "two", "People")],
)
def test_validation_messages(bill, percent, people, message):
    with pytest.raises(ValueError, match=message):
        calculate_tip(bill, percent, people)


@pytest.mark.gui
def test_widgets_are_built_with_grid():
    tk = pytest.importorskip("tkinter")
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display available")
    from src.day_48_tkinter_gui.main import TipApp

    try:
        app = TipApp(root)
        app.bill.set("50")
        app.people.set("2")
        app.calculate()
        assert "Each €" in app.output.get()
        app.bill.set("oops")
        app.calculate()
        assert app.output.get().startswith("⚠")
    finally:
        root.destroy()
