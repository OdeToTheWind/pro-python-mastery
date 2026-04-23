# tests/test_day_32.py
from src.day_32_class_initialisers.main import BankAccount

def test_bankaccount_initialiser():
    acc = BankAccount("Alice", 5000, "Current")
    assert acc.owner == "Alice"
    assert acc.balance == 5000.0
    assert acc.account_type == "Current"

def test_negative_initial_balance():
    acc = BankAccount("Bob", -100)
    assert acc.balance == 0.0  # protected by max(0.0, balance)

def test_deposit_withdraw():
    acc = BankAccount("Test", 1000)
    assert "Deposited" in acc.deposit(500)
    assert "Withdrew" in acc.withdraw(300)
    assert acc.balance == 1200.0