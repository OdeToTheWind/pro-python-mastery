"""Day 10 – Randomisation.

Scenario: a *board-game night toolkit* – dice, a card deck, a raffle and a
password generator for the Wi-Fi.

Deliverables (syllabus):
* The ``random`` module: ``randint()``, ``choice()``, ``shuffle()`` (and seeding)
* Password generation (with ``secrets`` – ``random`` is not cryptographically safe)
* Games
"""

from __future__ import annotations

import random
import secrets
import string
from collections.abc import Callable

DELIVERABLES: dict[str, str] = {
    "randint()": "roll_dice",
    "shuffle()": "deal_cards",
    "choice()": "pick_raffle_winner",
    "seeding for reproducibility": "roll_dice",
    "secure password generation": "generate_password",
    "game": "rock_paper_scissors",
}

SUITS = "♠♥♦♣"
RANKS = ["A", *map(str, range(2, 11)), "J", "Q", "K"]
BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
SYMBOLS = "!@#$%^&*-_=+?"


def roll_dice(count: int = 2, sides: int = 6, rng: random.Random | None = None) -> list[int]:
    """Roll *count* dice with ``randint`` (both ends inclusive)."""
    if count < 1 or sides < 2:
        raise ValueError("need at least one die with at least two sides")
    rng = rng or random.Random()
    return [rng.randint(1, sides) for _ in range(count)]


def new_deck() -> list[str]:
    return [f"{rank}{suit}" for suit in SUITS for rank in RANKS]


def deal_cards(players: int, cards_each: int, rng: random.Random | None = None) -> list[list[str]]:
    """Shuffle a fresh deck in place and deal round-robin."""
    deck = new_deck()
    if players * cards_each > len(deck):
        raise ValueError("not enough cards in one deck")
    (rng or random.Random()).shuffle(deck)
    return [deck[i : players * cards_each : players] for i in range(players)]


def pick_raffle_winner(tickets: dict[str, int], rng: random.Random | None = None) -> str:
    """Pick a winner with ``choice``; more tickets means better odds."""
    pool = [name for name, count in tickets.items() for _ in range(count)]
    if not pool:
        raise ValueError("nobody bought a ticket")
    return (rng or random.Random()).choice(pool)


def rock_paper_scissors(player: str, computer: str) -> str:
    """Pure game rule: return 'win', 'lose' or 'draw' for *player*."""
    player, computer = player.lower(), computer.lower()
    if player not in BEATS or computer not in BEATS:
        raise ValueError("choose rock, paper or scissors")
    if player == computer:
        return "draw"
    return "win" if BEATS[player] == computer else "lose"


def play_round(player: str, rng: random.Random | None = None) -> tuple[str, str]:
    computer = (rng or random.Random()).choice(list(BEATS))
    return computer, rock_paper_scissors(player, computer)


def generate_password(length: int = 16, *, symbols: bool = True) -> str:
    """Generate a password with the ``secrets`` CSPRNG.

    Guarantees at least one lowercase, uppercase, digit (and symbol), then
    shuffles with ``secrets.SystemRandom`` so their positions are not predictable.
    """
    classes = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
    if symbols:
        classes.append(SYMBOLS)
    if length < max(12, len(classes)):
        raise ValueError("passwords must be at least 12 characters")
    alphabet = "".join(classes)
    chars = [secrets.choice(group) for group in classes]
    chars += [secrets.choice(alphabet) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def main(ask: Callable[[str], str] | None = None) -> None:
    ask = ask or input
    seeded = random.Random(2026)
    print("Day 10 – Board-game night toolkit\n")
    print("Dice (seed 2026):", roll_dice(3, rng=seeded))
    print("Hands:", deal_cards(2, 5, rng=seeded))
    print("Raffle winner:", pick_raffle_winner({"Ada": 3, "Grace": 1}, rng=seeded))
    print("Wi-Fi password:", generate_password(16))
    print("\nRock-paper-scissors (blank to stop):")
    while True:
        try:
            move = ask("your move → ").strip()
        except EOFError:
            break
        if not move:
            break
        try:
            computer, outcome = play_round(move)
        except ValueError as exc:
            print(f"  ✗ {exc}")
            continue
        print(f"  computer chose {computer}: you {outcome}")


if __name__ == "__main__":
    main()
