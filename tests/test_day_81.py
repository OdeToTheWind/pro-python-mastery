"""Tests for Day 81 – Advanced Regular Expressions."""

import re
import time
from decimal import Decimal

import pytest

from src.day_81_advanced_regular_expressions.main import (
    SAFE_EMAIL_RE,
    SAMPLE,
    find_orders,
    find_repeated_words,
    is_strong_reference,
    main,
    normalise_whitespace,
    parse_amounts,
    parse_dates,
    redact,
    split_sentences,
    valid_order_number,
)


def test_find_orders_normalises_variants():
    assert [str(o) for o in find_orders(SAMPLE)] == ["ORD-2026-00417", "INV-2026-00999"]
    assert find_orders("ORD-1999-00001 ORD-2026-1234") == []  # wrong year range / too short


@pytest.mark.parametrize(("text", "ok"), [("ORD-2026-00417", True), ("ord 2026 00417", True),
                                          ("ORD-2026-00417x", False), ("see ORD-2026-00417", False)])
def test_fullmatch_validation(text, ok):
    assert valid_order_number(text) is ok


def test_amounts_with_lookbehind_and_formats():
    assert parse_amounts(SAMPLE) == [Decimal("1234.56"), Decimal("49.90")]
    assert parse_amounts("$1,299.00 and £5 and 12.50 USD") == [Decimal("1299.00"), Decimal("5"), Decimal("12.50")]
    assert parse_amounts("call 1234") == []  # no currency → not an amount


def test_dates_alternation():
    assert parse_dates("on 03.04.2026 and 2026-04-05 and 7/1/2026") == ["2026-04-03", "2026-04-05", "2026-01-07"]


def test_backreference_repeated_words():
    assert find_repeated_words(SAMPLE) == ["broken"]
    assert find_repeated_words("The the cat") == ["the"]
    assert find_repeated_words("no repeats here") == []


@pytest.mark.parametrize(("code", "strong"), [("Ticket-2026X", True), ("ticket-2026x", False),
                                              ("Password-1A", False), ("SHORT1A", False), ("AB-1234-CD", False)])
def test_lookahead_reference_rules(code, strong):
    assert is_strong_reference(code) is strong


def test_redaction_keeps_triage_hints():
    text = redact("Mail ada.lovelace@example.com or call +49 170 1234567 about ORD-2026-00417")
    assert text == "Mail a***@example.com or call [phone …67] about ORD-2026-00417"


def test_split_and_normalise():
    assert split_sentences("It broke. Can you help? thanks e.g. now! Done.") == [
        "It broke.", "Can you help? thanks e.g. now!", "Done."]
    assert normalise_whitespace("a   b\n\n\n\nc") == "a b\n\nc"


def test_safe_email_pattern_is_fast_on_hostile_input():
    hostile = "a" * 50_000 + "@"
    start = time.perf_counter()
    assert SAFE_EMAIL_RE.search(hostile) is None
    assert time.perf_counter() - start < 1.0


def test_patterns_compile_with_flags():
    from src.day_81_advanced_regular_expressions.main import ORDER_RE

    assert ORDER_RE.flags & re.VERBOSE and ORDER_RE.flags & re.IGNORECASE
    assert set(ORDER_RE.groupindex) == {"prefix", "year", "number"}


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "a***@example.com" in out and "orders : ['ORD-2026-00417', 'INV-2026-00999']" in out
