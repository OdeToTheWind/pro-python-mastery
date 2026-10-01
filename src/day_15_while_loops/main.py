"""Day 15 – While Loops.

Scenario: an *arcade cabinet* – a number-guessing game, a PIN lock and a
coin-counting machine, each driven by ``while`` loops.

Deliverables (syllabus):
* ``while`` loops
* ``break`` and ``continue``
* ``while ... else``
* Input validation
* Games
"""

from __future__ import annotations

import ast
import operator
import random
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field

DELIVERABLES: dict[str, str] = {
    "while loop": "collatz_steps",
    "break": "guessing_game",
    "continue": "count_coins",
    "while ... else": "unlock",
    "input validation loop": "ask_int",
    "game": "guessing_game",
    "safe calculator (replaces eval)": "safe_eval",
}

COIN_VALUES = {"1c": 1, "2c": 2, "5c": 5, "10c": 10, "20c": 20, "50c": 50, "1e": 100, "2e": 200}


def collatz_steps(n: int) -> int:
    """Count steps until *n* reaches 1 – we can't know the count in advance, so ``while``."""
    if n < 1:
        raise ValueError("n must be positive")
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    return steps


def count_coins(inserted: list[str]) -> tuple[int, list[str]]:
    """Total valid coins; ``continue`` skips rejects, ``break`` stops at 'STOP'."""
    total, rejected = 0, []
    index = 0
    while index < len(inserted):
        coin = inserted[index]
        index += 1
        if coin == "STOP":
            break
        if coin not in COIN_VALUES:
            rejected.append(coin)
            continue
        total += COIN_VALUES[coin]
    return total, rejected


@dataclass
class GameResult:
    won: bool
    attempts: int
    hints: list[str] = field(default_factory=list)


def guessing_game(secret: int, guesses: Iterator[int], max_attempts: int = 7) -> GameResult:
    """Higher/lower game. ``break`` exits on a correct guess."""
    result = GameResult(won=False, attempts=0)
    while result.attempts < max_attempts:
        try:
            guess = next(guesses)
        except StopIteration:
            break
        result.attempts += 1
        if guess == secret:
            result.won = True
            break
        result.hints.append("higher" if guess < secret else "lower")
    return result


def unlock(correct_pin: str, attempts: Iterator[str], max_tries: int = 3) -> str:
    """``while ... else``: the ``else`` block runs only if the loop never hit ``break``."""
    tries = 0
    while tries < max_tries:
        tries += 1
        if next(attempts, None) == correct_pin:
            message = f"unlocked after {tries} attempt(s)"
            break
    else:
        message = "locked out"
    return message


def ask_int(prompt: str, low: int, high: int, ask: Callable[[str], str]) -> int | None:
    """Keep asking until an integer in range is typed; ``None`` on EOF."""
    while True:
        try:
            text = ask(prompt)
        except EOFError:
            return None
        if not text.strip().lstrip("-").isdigit():
            print("  ✗ whole numbers only")
            continue
        value = int(text)
        if low <= value <= high:
            return value
        print(f"  ✗ between {low} and {high}, please")


_BIN_OPS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}


def safe_eval(expression: str, max_exponent: int = 100) -> float:
    """Evaluate arithmetic safely by walking the AST.

    The previous version used ``eval`` with empty builtins, which is *not* a
    sandbox (``().__class__.__base__.__subclasses__()`` escapes it, and
    ``9**9**9`` hangs the process). Only numbers and arithmetic are allowed here.
    """

    def visit(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if (isinstance(node, ast.Constant) and isinstance(node.value, int | float)
                and not isinstance(node.value, bool)):
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub | ast.UAdd):
            value = visit(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp) and type(node.op) in _BIN_OPS:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > max_exponent:
                raise ValueError("exponent too large")
            return _BIN_OPS[type(node.op)](left, right)
        raise ValueError(f"unsupported expression element: {type(node).__name__}")

    return visit(ast.parse(expression, mode="eval"))


def main(ask: Callable[[str], str] | None = None) -> None:
    ask = ask or input
    print("Day 15 – Arcade cabinet\n")
    print("Collatz steps for 27:", collatz_steps(27))
    print("Coins:", count_coins(["1e", "bottle-cap", "50c", "STOP", "2e"]))
    print("PIN:", unlock("2468", iter(["1111", "2468"])))
    print("Calculator 2 + 3 * 4 =", safe_eval("2 + 3 * 4"))

    secret = random.randint(1, 50)
    print("\nGuess my number between 1 and 50 (Ctrl-D to give up)")
    attempts = 0
    while (guess := ask_int("guess → ", 1, 50, ask)) is not None:
        attempts += 1
        if guess == secret:
            print(f"🎉 Correct in {attempts} attempt(s)!")
            break
        print("  higher" if guess < secret else "  lower")
    else:
        print(f"The number was {secret}.")


if __name__ == "__main__":
    main()
