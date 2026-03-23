# tests/test_day_10.py
import pytest
import random
from src.day_10_randomisation.main import coin_flip, roll_dice, generate_password


def test_coin_flip():
    result = coin_flip()
    assert result in ["Heads", "Tails"]


def test_roll_dice():
    result = roll_dice(6)
    assert 1 <= result <= 6
    
    result_20 = roll_dice(20)
    assert 1 <= result_20 <= 20


def test_generate_password():
    pwd = generate_password(8)
    assert len(pwd) == 8
    assert any(c.isupper() for c in pwd)
    assert any(c.islower() for c in pwd)
    assert any(c.isdigit() for c in pwd)


def test_reproducibility_with_seed():
    random.seed(12345)
    first_run = random.randint(1, 1000)
    
    random.seed(12345)
    second_run = random.randint(1, 1000)
    
    assert first_run == second_run