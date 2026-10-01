"""Tests for Day 43 – CSV."""

from datetime import date
from decimal import Decimal

import pytest

from src.day_43_reading_writing_csv.main import (
    SAMPLE,
    Expense,
    detect_delimiter,
    export_summary,
    main,
    parse_expenses,
    parse_row,
    read_expenses,
    totals_by_category,
    write_expenses,
)


def test_parse_semicolon_export_with_quotes():
    expenses, errors = parse_expenses(SAMPLE)
    assert [e.description for e in expenses] == ["Groceries; weekly", "Bus pass", 'Dinner, "La Piazza"']
    assert expenses[2].amount == Decimal("1034.50")
    assert errors == ["line 4: bad amount 'not-a-number'", "line 6: missing description"]


def test_parse_comma_export():
    expenses, errors = parse_expenses("date,description,category,amount\n2026-01-01,Tea,food,3\n")
    assert expenses == [Expense(date(2026, 1, 1), "Tea", "food", Decimal("3"))]
    assert errors == []


def test_header_is_required():
    with pytest.raises(ValueError, match="header"):
        parse_expenses("a,b\n1,2\n")


@pytest.mark.parametrize(
    "row",
    [{"date": "2026-13-01", "description": "x", "category": "c", "amount": "1"},
     {"date": "2026-01-01", "description": "x", "category": "c", "amount": "-5"}],
)
def test_parse_row_rejects(row):
    with pytest.raises(ValueError):
        parse_row(row)


def test_write_and_read_round_trip(tmp_path):
    expenses, _ = parse_expenses(SAMPLE)
    path = tmp_path / "clean.csv"
    write_expenses(path, expenses)
    assert read_expenses(path) == (expenses, [])
    assert path.read_text(encoding="utf-8").splitlines()[0] == "date,description,category,amount"


def test_read_tolerates_excel_bom(tmp_path):
    path = tmp_path / "bom.csv"
    path.write_text("﻿date,description,category,amount\n2026-01-01,a,b,1\n", encoding="utf-8")
    assert len(read_expenses(path)[0]) == 1


def test_totals_and_summary_export(tmp_path):
    expenses, _ = parse_expenses(SAMPLE)
    assert totals_by_category(expenses) == {"food": Decimal("1116.90"), "transport": Decimal("45.00")}
    out = tmp_path / "summary.csv"
    export_summary(out, expenses)
    assert out.read_text(encoding="utf-8").splitlines() == [
        "category,total,share", "food,1116.90,96.1%", "transport,45.00,3.9%",
    ]


def test_main(capsys, tmp_path):
    main(tmp_path)
    assert "food,1116.90,96.1%" in capsys.readouterr().out


def test_detect_delimiter():
    assert detect_delimiter("a;b;c\n") == ";"
    assert detect_delimiter("a,b,c\n") == ","
    assert detect_delimiter("a\tb\tc\n") == "\t"
    assert detect_delimiter("") == ","
