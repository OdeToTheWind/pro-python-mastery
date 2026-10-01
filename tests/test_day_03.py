"""Tests for Day 03 – Input & Print Functions."""

import pytest

from src.day_03_input_output.main import (
    Registration,
    RegistrationCancelled,
    ask,
    format_receipt,
    main,
    non_empty,
    one_of,
    register,
    to_int_in_range,
)


def answers(*values):
    queue = list(values)

    def fake(_prompt: str) -> str:
        if not queue:
            raise EOFError
        return queue.pop(0)

    return fake


def test_to_int_in_range_accepts_bounds():
    assert to_int_in_range("12", 12, 120) == 12
    assert to_int_in_range("120", 12, 120) == 120


@pytest.mark.parametrize("text", ["11", "121", "abc", "4.5", ""])
def test_to_int_in_range_rejects(text):
    with pytest.raises(ValueError):
        to_int_in_range(text, 12, 120)


def test_non_empty_and_one_of():
    assert non_empty("  Ada   Lovelace ") == "Ada Lovelace"
    assert one_of("a", "b")("B") == "b"
    with pytest.raises(ValueError):
        one_of("a")("z")


def test_ask_retries_then_succeeds():
    messages: list[str] = []
    value = ask("Age: ", int, ask_fn=answers("x", "7"), print_fn=messages.append)
    assert value == 7
    assert len(messages) == 1 and "2 attempt(s) left" in messages[0]


def test_ask_gives_up_after_max_attempts():
    with pytest.raises(RegistrationCancelled, match="too many"):
        ask("Age: ", int, ask_fn=answers("a", "b"), print_fn=lambda _m: None, max_attempts=2)


def test_ask_turns_eof_into_cancellation_instead_of_looping():
    with pytest.raises(RegistrationCancelled, match="closed"):
        ask("Name: ", str, ask_fn=answers(), print_fn=print)


def test_ask_cancel_keyword():
    with pytest.raises(RegistrationCancelled, match="cancelled"):
        ask("Name: ", str, ask_fn=answers("CANCEL"))


def test_register_uses_age_based_default_ticket():
    reg = register(answers("  ada  lovelace", "19", "", ""), print_fn=lambda _m: None)
    assert reg == Registration("ada lovelace", 19, "student", 0)


def test_registration_total_and_receipt():
    reg = Registration("Ada", 30, "vip", 2)
    assert reg.total == pytest.approx(285.0)
    receipt = format_receipt(reg)
    assert "VIP" in receipt
    assert "€  285.00" in receipt
    header = receipt.splitlines()[0]
    assert len(header) == 36 and " RECEIPT " in header and header.strip("=") == " RECEIPT "


def test_main_full_flow():
    out: list[str] = []
    main(answers("Grace", "40", "standard", "1"), out.append)
    assert "€   80.00" in out[-1]


def test_main_reports_cancellation():
    out: list[str] = []
    main(answers("Grace"), out.append)
    assert out[-1].startswith("Registration cancelled")
