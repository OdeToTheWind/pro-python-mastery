# src/day_38_game_development_with_python_and_oop/main.py
"""
Day 38: Game Development with Python and OOP – Simple Text Adventure
"""

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []

    def attack(self, enemy):
        damage = 25
        enemy.health -= damage
        print(f"{self.name} attacks {enemy.name} for {damage} damage!")

    def heal(self):
        self.health = min(100, self.health + 30)
        print(f"{self.name} healed. Health now: {self.health}")


class Enemy:
    def __init__(self, name, health=60):
        self.name = name
        self.health = health

    def is_defeated(self):
        return self.health <= 0


def main():
    print("Welcome to Day 38 – Simple Text Game using OOP\n")

    player = Player("Hero")
    goblin = Enemy("Goblin", 70)

    print(f"You encounter a wild {goblin.name}!\n")

    while player.health > 0 and not goblin.is_defeated():
        print(f"Your Health: {player.health} | Goblin Health: {goblin.health}")
        action = input("Choose action (attack/heal): ").strip().lower()

        if action == "attack":
            player.attack(goblin)
        elif action == "heal":
            player.heal()
        else:
            print("Invalid action! Try 'attack' or 'heal'.")

    if goblin.is_defeated():
        print(f"\n🎉 You defeated the {goblin.name}!")
    else:
        print("\n💀 You were defeated...")

    print("\nThis is a basic example of using OOP for game development.")
    print("Next: Python Inheritance (Day 39)\n")


if __name__ == "__main__":
    main()