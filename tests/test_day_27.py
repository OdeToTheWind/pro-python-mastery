"""Tests for Day 27 – Object-Oriented Programming."""

from decimal import Decimal

import pytest

from src.day_27_oop_basics.main import (
    CreditCard,
    PaymentDeclined,
    PaymentMethod,
    Wallet,
    checkout,
    main,
)


@pytest.fixture
def card():
    return CreditCard("Ada", "4111 1111 1111 1111", Decimal("100"))


def test_abstract_class_cannot_be_instantiated():
    with pytest.raises(TypeError, match="abstract"):
        PaymentMethod("x")  # type: ignore[abstract]


def test_incomplete_subclass_is_still_abstract():
    class Half(PaymentMethod):
        def describe(self):
            return "half"

    with pytest.raises(TypeError):
        Half("x")


def test_card_encapsulation(card):
    assert card.masked_number == "•••• 1111"
    assert not hasattr(card, "__number")
    assert card._CreditCard__number == "4111111111111111"  # name mangling, not true privacy
    assert "4111 1111" not in repr(card)


def test_card_validation():
    with pytest.raises(ValueError):
        CreditCard("Ada", "12ab", Decimal("1"))


def test_card_limit(card):
    assert card.pay(Decimal("60")).reference.startswith("CC-1111")
    assert card.available == Decimal("40")
    with pytest.raises(PaymentDeclined):
        card.pay(Decimal("41"))


def test_wallet_read_only_balance():
    wallet = Wallet("Grace", Decimal("10"))
    with pytest.raises(AttributeError):
        wallet.balance = Decimal("1000")  # type: ignore[misc]
    wallet.top_up(Decimal("5"))
    assert wallet.balance == Decimal("15")
    with pytest.raises(ValueError):
        wallet.top_up(Decimal("0"))


def test_shared_validation_in_base_class(card):
    with pytest.raises(ValueError):
        card.pay(Decimal("0"))


def test_polymorphic_checkout(card):
    wallet = Wallet("Grace", Decimal("20"))
    assert checkout(card, Decimal("30")) == "paid 30 via Card •••• 1111"
    assert checkout(wallet, Decimal("25")) == "declined (insufficient wallet balance)"
    assert checkout(wallet, Decimal("20")) == "paid 20 via Wallet of Grace"
    assert wallet.balance == 0


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "Abstract class:" in out and "declined" in out
