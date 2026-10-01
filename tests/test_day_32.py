"""Tests for Day 32 – Class Initialisers."""

from decimal import Decimal

import pytest

from src.day_32_class_initialisers.main import BadAccount, BankAccount, SavingsGoal, main


def test_defaults_and_setup():
    account = BankAccount("  Ada   Lovelace ")
    assert account.owner == "Ada Lovelace"
    assert account.account_type == "savings"
    assert account.balance == 0 and account.transactions == []


def test_unique_account_numbers():
    a, b = BankAccount("A"), BankAccount("B")
    assert b.number == a.number + 1


@pytest.mark.parametrize(
    ("args", "message"),
    [(("",), "owner"), (("Eve", Decimal("-1")), "negative"), (("Eve", Decimal("0"), "gold"), "account_type")],
)
def test_constructor_rejects_invalid_state(args, message):
    with pytest.raises(ValueError, match=message):
        BankAccount(*args)


def test_each_account_gets_its_own_list():
    a, b = BankAccount("A"), BankAccount("B")
    a.deposit(Decimal("5"))
    assert b.transactions == []


def test_caller_list_is_copied():
    history = [Decimal("10")]
    account = BankAccount("A", transactions=history)
    account.deposit(Decimal("1"))
    assert history == [Decimal("10")]


def test_deposit_and_withdraw_validation():
    account = BankAccount("A", Decimal("100"))
    assert account.withdraw(Decimal("40")) == Decimal("60")
    for bad in (Decimal("0"), Decimal("-5")):
        with pytest.raises(ValueError):
            account.deposit(bad)
        with pytest.raises(ValueError):
            account.withdraw(bad)
    with pytest.raises(ValueError, match="insufficient"):
        account.withdraw(Decimal("61"))


def test_mutable_default_trap_is_demonstrated():
    one, two = BadAccount("x"), BadAccount("y")
    one.transactions.append(1)
    assert two.transactions == [1]  # the bug the None-sentinel avoids
    one.transactions.clear()


def test_savings_goal_post_init():
    goal = SavingsGoal("bike", Decimal("400"), Decimal("100"))
    assert goal.progress == 0.25 and goal.contributions == []
    with pytest.raises(ValueError):
        SavingsGoal("x", Decimal("0"))
    with pytest.raises(ValueError):
        SavingsGoal("x", Decimal("10"), Decimal("11"))


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "Rejected 'Eve': opening balance cannot be negative" in out
    assert "second object sees: [99]" in out
