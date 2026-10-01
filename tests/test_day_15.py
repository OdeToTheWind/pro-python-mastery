"""Tests for Day 15 – While Loops."""

import pytest

from src.day_15_while_loops import main as day15
from src.day_15_while_loops.main import (
    ask_int,
    collatz_steps,
    count_coins,
    guessing_game,
    safe_eval,
    unlock,
)


@pytest.mark.parametrize(("n", "steps"), [(1, 0), (2, 1), (6, 8), (27, 111)])
def test_collatz_steps(n, steps):
    assert collatz_steps(n) == steps


def test_collatz_rejects_non_positive():
    with pytest.raises(ValueError):
        collatz_steps(0)


def test_count_coins_continue_and_break():
    assert count_coins(["1e", "button", "50c", "STOP", "2e"]) == (150, ["button"])
    assert count_coins([]) == (0, [])


def test_guessing_game_win_and_hints():
    result = guessing_game(42, iter([10, 60, 42, 1]))
    assert result.won and result.attempts == 3
    assert result.hints == ["higher", "lower"]


def test_guessing_game_runs_out_of_attempts():
    result = guessing_game(5, iter([1] * 10), max_attempts=3)
    assert not result.won and result.attempts == 3


def test_guessing_game_runs_out_of_guesses():
    assert guessing_game(5, iter([1])).attempts == 1


def test_while_else():
    assert unlock("1234", iter(["0000", "1234"])) == "unlocked after 2 attempt(s)"
    assert unlock("1234", iter(["0", "1", "2", "1234"])) == "locked out"
    assert unlock("1234", iter([])) == "locked out"


def _answers(*values):
    queue = list(values)

    def fake(_prompt):
        if not queue:
            raise EOFError
        return queue.pop(0)

    return fake


def test_ask_int_validates(capsys):
    assert ask_int("n: ", 1, 10, _answers("abc", "99", "7")) == 7
    out = capsys.readouterr().out
    assert "whole numbers only" in out and "between 1 and 10" in out
    assert ask_int("n: ", 1, 10, _answers()) is None


@pytest.mark.parametrize(
    ("expr", "value"), [("2 + 3 * 4", 14), ("(2 + 3) * 4", 20), ("-2 ** 2", -4), ("7 // 2", 3),
                        ("2 ** 10", 1024), ("+5 % 3", 2)],
)
def test_safe_eval_arithmetic(expr, value):
    assert safe_eval(expr) == value


@pytest.mark.parametrize(
    "attack",
    ["().__class__.__base__.__subclasses__()", "__import__('os').system('echo hi')",
     "9 ** 9 ** 9", "open('x')", "'a' * 3", "[1, 2]", "True + 1"],
)
def test_safe_eval_blocks_code_execution(attack):
    with pytest.raises(ValueError):
        safe_eval(attack)


def test_safe_eval_syntax_error():
    with pytest.raises(SyntaxError):
        safe_eval("2 +")


def test_main_game(capsys, scripted_input, monkeypatch):
    monkeypatch.setattr(day15.random, "randint", lambda _a, _b: 20)
    scripted_input(["10", "30", "20"])
    day15.main()
    out = capsys.readouterr().out
    assert "Correct in 3 attempt(s)" in out


def test_main_give_up(capsys, scripted_input, monkeypatch):
    monkeypatch.setattr(day15.random, "randint", lambda _a, _b: 20)
    scripted_input([])
    day15.main()
    assert "The number was 20." in capsys.readouterr().out
