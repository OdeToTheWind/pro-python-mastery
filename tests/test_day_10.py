"""Tests for Day 10 – Randomisation."""

import random
import string

import pytest

from src.day_10_randomisation.main import (
    SYMBOLS,
    deal_cards,
    generate_password,
    main,
    new_deck,
    pick_raffle_winner,
    play_round,
    rock_paper_scissors,
    roll_dice,
)


def test_roll_dice_range_and_reproducibility():
    rolls = roll_dice(100, sides=6, rng=random.Random(1))
    assert all(1 <= r <= 6 for r in rolls)
    assert set(rolls) == {1, 2, 3, 4, 5, 6}
    assert roll_dice(5, rng=random.Random(7)) == roll_dice(5, rng=random.Random(7))


@pytest.mark.parametrize(("count", "sides"), [(0, 6), (1, 1), (1, 0)])
def test_roll_dice_validation(count, sides):
    with pytest.raises(ValueError):
        roll_dice(count, sides)


def test_deck_has_52_unique_cards():
    deck = new_deck()
    assert len(deck) == len(set(deck)) == 52


def test_deal_cards_unique_and_sized():
    hands = deal_cards(4, 13, rng=random.Random(3))
    dealt = [card for hand in hands for card in hand]
    assert [len(h) for h in hands] == [13] * 4
    assert sorted(dealt) == sorted(new_deck())


def test_deal_cards_too_many():
    with pytest.raises(ValueError):
        deal_cards(6, 10)


def test_raffle_respects_ticket_weights():
    rng = random.Random(0)
    wins = [pick_raffle_winner({"Ada": 9, "Grace": 1}, rng=rng) for _ in range(500)]
    assert wins.count("Ada") > wins.count("Grace") * 4


def test_raffle_without_tickets():
    with pytest.raises(ValueError):
        pick_raffle_winner({"Ada": 0})


@pytest.mark.parametrize(
    ("player", "computer", "outcome"),
    [("rock", "scissors", "win"), ("paper", "scissors", "lose"), ("Scissors", "scissors", "draw"),
     ("paper", "rock", "win")],
)
def test_rock_paper_scissors_rules(player, computer, outcome):
    assert rock_paper_scissors(player, computer) == outcome


def test_rock_paper_scissors_invalid():
    with pytest.raises(ValueError):
        rock_paper_scissors("lizard", "rock")


def test_play_round_is_consistent():
    computer, outcome = play_round("rock", rng=random.Random(5))
    assert outcome == rock_paper_scissors("rock", computer)


@pytest.mark.parametrize("length", [12, 16, 40])
def test_password_contains_every_character_class(length):
    pwd = generate_password(length)
    assert len(pwd) == length
    assert any(c in string.ascii_lowercase for c in pwd)
    assert any(c in string.ascii_uppercase for c in pwd)
    assert any(c in string.digits for c in pwd)
    assert any(c in SYMBOLS for c in pwd)


def test_password_without_symbols_and_minimum_length():
    assert not any(c in SYMBOLS for c in generate_password(20, symbols=False))
    with pytest.raises(ValueError):
        generate_password(8)


def test_passwords_are_not_repeated():
    assert len({generate_password() for _ in range(50)}) == 50


def test_main(capsys, scripted_input):
    scripted_input(["rock", "lizard", ""])
    main()
    out = capsys.readouterr().out
    assert "computer chose" in out
    assert "choose rock, paper or scissors" in out
