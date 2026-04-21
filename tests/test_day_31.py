# tests/test_day_31.py
from src.day_31_python_methods.main import BankAccount

def test_bank_account_instance_methods():
    acc = BankAccount("Test", 500)
    assert acc.deposit(300) == "Deposited ₹300. New balance: ₹800"
    assert acc.withdraw(200) == "Withdrew ₹200. New balance: ₹600"

def test_static_method():
    assert BankAccount.is_valid_amount(100) is True
    assert BankAccount.is_valid_amount(-50) is False

def test_class_method():
    BankAccount.set_interest_rate(0.07)
    assert BankAccount.interest_rate == 0.07