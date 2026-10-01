"""Tests for Day 38 – Game Development with OOP."""

import random

import pytest

from src.day_38_game_development_with_python_and_oop.main import (
    Battle,
    Character,
    Hero,
    main,
    new_battle,
    play,
)


def test_take_damage_never_goes_below_zero():
    c = Character("x", 10, (1, 1))
    assert c.take_damage(25) == 10
    assert c.hp == 0 and not c.alive
    with pytest.raises(ValueError):
        c.take_damage(-5)


def test_heal_is_capped_and_limited():
    hero = Hero("h", 100, (1, 1), potions=1)
    hero.take_damage(10)
    assert hero.heal() == 10 and hero.hp == 100
    with pytest.raises(RuntimeError):
        hero.heal()


def test_monster_strikes_back():
    battle = Battle(Hero("h", 50, (1, 1)), Character("m", 50, (5, 5)), random.Random(0))
    battle.hero_turn("attack")
    assert battle.hero.hp == 45
    assert battle.log == ["h hits m for 1", "m strikes back for 5"]


def test_hero_can_lose():
    battle = Battle(Hero("h", 10, (1, 1), potions=0), Character("m", 100, (20, 20)), random.Random(0))
    battle.hero_turn("attack")
    assert battle.winner == "m"
    with pytest.raises(RuntimeError, match="over"):
        battle.hero_turn("attack")


def test_dead_monster_does_not_strike_back():
    battle = Battle(Hero("h", 10, (50, 50)), Character("m", 5, (20, 20)), random.Random(0))
    battle.hero_turn("attack")
    assert battle.winner == "h" and battle.hero.hp == 10


def test_invalid_action():
    with pytest.raises(ValueError):
        new_battle(1).hero_turn("dance")


def test_seeded_battles_are_reproducible():
    def run(seed):
        battle = new_battle(seed)
        while battle.winner is None:
            battle.hero_turn("attack")
        return battle.winner, battle.turns, battle.hero.hp

    assert run(42) == run(42)


def _answers(*values):
    queue = list(values)

    def fake(_prompt):
        if not queue:
            raise EOFError
        return queue.pop(0)

    return fake


def test_play_loop_handles_errors_and_finishes(capsys):
    battle = Battle(Hero("h", 30, (40, 40), potions=0), Character("m", 30, (1, 1)), random.Random(0))
    assert play(battle, _answers("heal", "jump", "attack")) == "h"
    out = capsys.readouterr().out
    assert "no potions left" in out and "action must be" in out


def test_main_abandoned(capsys, scripted_input):
    scripted_input([])
    main()
    assert "Result: abandoned" in capsys.readouterr().out
