# src/day_36_python_instances_and_state/main.py
"""
Day 36: Python Instances and State – Interactive Explorer
Understanding how each object maintains its own state.
"""

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.inventory = []
        self.level = 1
        print(f"Player '{name}' created with full health.")

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            print(f"{self.name} has been defeated!")
            return False
        print(f"{self.name} took {damage} damage. Health left: {self.health}")
        return True

    def add_item(self, item):
        self.inventory.append(item)
        print(f"{self.name} picked up: {item}")

    def show_status(self):
        print(f"\n--- {self.name}'s Status ---")
        print(f"Health: {self.health}")
        print(f"Level: {self.level}")
        print(f"Inventory: {self.inventory if self.inventory else 'Empty'}")
        print("------------------------")


def main():
    print("Welcome to Day 36 – Python Instances and State\n")
    print("Each object maintains its own independent state.\n")

    player1 = Player("Warrior")
    player2 = Player("Mage")

    while True:
        print("\n" + "─" * 60)
        print("Choose action:")
        print("  1) Show Player Status")
        print("  2) Deal Damage to a Player")
        print("  3) Add Item to Inventory")
        print("  4) Level Up a Player")
        print("  5) Exit")
        print("─" * 60)

        choice = input("→ ").strip()

        if choice == "5":
            break

        if choice == "1":
            p = player1 if input("Which player? (1 or 2): ") == "1" else player2
            p.show_status()

        elif choice == "2":
            p = player1 if input("Which player? (1 or 2): ") == "1" else player2
            dmg = int(input("Damage amount: "))
            p.take_damage(dmg)

        elif choice == "3":
            p = player1 if input("Which player? (1 or 2): ") == "1" else player2
            item = input("Item name: ").strip()
            p.add_item(item)

        elif choice == "4":
            p = player1 if input("Which player? (1 or 2): ") == "1" else player2
            p.level += 1
            print(f"{p.name} leveled up to level {p.level}!")

    print("\nYou now understand how each instance maintains its own state.")
    print("Next: Python Turtle (Day 37)\n")


if __name__ == "__main__":
    main()