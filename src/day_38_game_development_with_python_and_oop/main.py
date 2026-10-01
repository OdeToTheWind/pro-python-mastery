"""Day 38 – Game Development with Python and OOP.

Scenario: *Dungeon Duel* – a turn-based battle between a hero and monsters.
Both sides attack, the hero can heal with limited potions, and the battle can
be won **or lost**. Randomness is injected so games are reproducible in tests.

Deliverables (syllabus):
* Simple game-building using classes
* Game state (health, potions, turn log, winner)
* User interaction (command loop)
"""

from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass, field

DELIVERABLES: dict[str, str] = {
    "game classes": "Character",
    "player-specific behaviour": "Hero",
    "game state and turn logic": "Battle",
    "enemy AI (counter-attacks)": "Battle.enemy_turn",
    "user interaction loop": "play",
}


@dataclass
class Character:
    name: str
    max_hp: int
    attack_range: tuple[int, int]
    hp: int = field(init=False)

    def __post_init__(self) -> None:
        self.hp = self.max_hp

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("damage cannot be negative")
        dealt = min(self.hp, amount)
        self.hp -= dealt
        return dealt

    def attack(self, target: Character, rng: random.Random) -> int:
        return target.take_damage(rng.randint(*self.attack_range))


@dataclass
class Hero(Character):
    potions: int = 2
    heal_amount: int = 30

    def heal(self) -> int:
        if self.potions == 0:
            raise RuntimeError("no potions left")
        self.potions -= 1
        healed = min(self.heal_amount, self.max_hp - self.hp)
        self.hp += healed
        return healed


@dataclass
class Battle:
    hero: Hero
    monster: Character
    rng: random.Random = field(default_factory=random.Random)
    log: list[str] = field(default_factory=list)
    turns: int = 0

    @property
    def winner(self) -> str | None:
        if not self.monster.alive:
            return self.hero.name
        if not self.hero.alive:
            return self.monster.name
        return None

    def hero_turn(self, action: str) -> None:
        if self.winner:
            raise RuntimeError("the battle is over")
        if action == "attack":
            dealt = self.hero.attack(self.monster, self.rng)
            self.log.append(f"{self.hero.name} hits {self.monster.name} for {dealt}")
        elif action == "heal":
            healed = self.hero.heal()
            self.log.append(f"{self.hero.name} drinks a potion (+{healed} HP)")
        else:
            raise ValueError("action must be 'attack' or 'heal'")
        self.turns += 1
        if self.monster.alive:
            self.enemy_turn()

    def enemy_turn(self) -> None:
        dealt = self.monster.attack(self.hero, self.rng)
        self.log.append(f"{self.monster.name} strikes back for {dealt}")


def status(battle: Battle) -> str:
    h, m = battle.hero, battle.monster
    return f"{h.name} {h.hp}/{h.max_hp} HP ({h.potions} potions) | {m.name} {m.hp}/{m.max_hp} HP"


def play(battle: Battle, ask: Callable[[str], str]) -> str:
    """Interactive loop; returns the winner (or 'abandoned' on EOF)."""
    while battle.winner is None:
        print(status(battle))
        try:
            action = ask("attack / heal → ").strip().lower()
        except EOFError:
            return "abandoned"
        try:
            battle.hero_turn(action)
        except (ValueError, RuntimeError) as exc:
            print(f"  ✗ {exc}")
            continue
        print("  " + " | ".join(battle.log[-2:]))
    return battle.winner


def new_battle(seed: int | None = None) -> Battle:
    return Battle(Hero("Hero", 100, (12, 20)), Character("Goblin King", 90, (8, 16)), random.Random(seed))


def main(ask: Callable[[str], str] | None = None) -> None:
    print("Day 38 – Dungeon Duel\n")
    winner = play(new_battle(), ask or input)
    print(f"\nResult: {winner}")


if __name__ == "__main__":
    main()
