# src/day_10_randomisation/main.py
"""
Day 10: Randomisation in Python – Interactive Playground
Explore random module functions with user-driven mini-games and tools.
"""

import random


def print_random_cheat_sheet():
    print("\n" + "═" * 70)
    print("Python random Module – Quick Reference (Day 10)")
    print("═" * 70)
    print("Function              | Purpose                              | Returns                  | Example")
    print("──────────────────────┼──────────────────────────────────────┼──────────────────────────┼──────────────────────────────")
    print("random.random()       | Float between 0.0 and 1.0 (inclusive) | float [0.0, 1.0)        | random.random() → 0.374448")
    print("random.randint(a, b)  | Integer from a to b (both inclusive)  | int                     | random.randint(1, 6) → 4")
    print("random.randrange(start, stop[, step]) | Integer from start to stop-1 | int               | random.randrange(0, 10, 2) → 6")
    print("random.choice(seq)    | Single random element from sequence   | element                 | random.choice(['rock', 'paper', 'scissors'])")
    print("random.choices(seq, k=n) | n random elements with replacement | list                | random.choices(['A','B','C'], k=5)")
    print("random.shuffle(seq)   | Shuffle list in place                 | None (modifies seq)     | random.shuffle(deck)")
    print("random.seed(a)        | Set seed for reproducibility          | None                    | random.seed(42) – same results every time")
    print("═" * 70)
    print("Tip: Never use random for cryptography (use secrets module instead)")
    print("═" * 70)


def coin_flip() -> str:
    return random.choice(["Heads", "Tails"])


def roll_dice(sides: int = 6) -> int:
    return random.randint(1, sides)


def rock_paper_scissors(player_choice: str) -> str:
    choices = ["rock", "paper", "scissors"]
    computer = random.choice(choices)
    
    if player_choice.lower() not in choices:
        return "Invalid choice! Pick rock, paper, or scissors."
    
    if player_choice.lower() == computer:
        return f"Computer chose {computer}. It's a tie!"
    elif (player_choice.lower() == "rock" and computer == "scissors") or \
         (player_choice.lower() == "paper" and computer == "rock") or \
         (player_choice.lower() == "scissors" and computer == "paper"):
        return f"Computer chose {computer}. You win!"
    else:
        return f"Computer chose {computer}. You lose!"


def generate_password(length: int = 12) -> str:
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    return ''.join(random.choices(chars, k=length))


def main():
    print("Welcome to Day 10 – Randomisation Playground!")
    print("Play games, generate passwords, roll dice — all powered by randomness.\n")

    print_random_cheat_sheet()

    while True:
        print("\n" + "─" * 60)
        print("Choose an activity (or 'quit' to exit):")
        print("  1) Coin flip")
        print("  2) Roll dice")
        print("  3) Rock-Paper-Scissors vs computer")
        print("  4) Generate random password")
        print("  5) Random choice from your list")
        print("  6) Show seed demo (reproducibility)")
        print("─" * 60)

        choice = input("→ ").strip().lower()

        if choice in ('quit', 'q', 'exit'):
            break

        if choice == '1':
            print(f"\n→ Coin flip result: {coin_flip()}")
        
        elif choice == '2':
            sides = input("How many sides? (default 6): ").strip()
            sides = int(sides) if sides.isdigit() else 6
            print(f"\n→ You rolled a {sides}-sided die: {roll_dice(sides)}")
        
        elif choice == '3':
            player = input("Choose rock, paper, or scissors: ").strip()
            print("\n" + rock_paper_scissors(player))
        
        elif choice == '4':
            length_str = input("Password length (default 12): ").strip()
            length = int(length_str) if length_str.isdigit() else 12
            pwd = generate_password(length)
            print(f"\n→ Generated password: {pwd}")
        
        elif choice == '5':
            items = input("Enter items separated by comma: ").strip()
            if not items:
                print("No items entered.")
                continue
            item_list = [x.strip() for x in items.split(',')]
            winner = random.choice(item_list)
            print(f"\n→ From your list: {winner!r} was chosen!")
        
        elif choice == '6':
            seed_val = input("Enter seed number (e.g. 42): ").strip()
            if seed_val.isdigit():
                random.seed(int(seed_val))
                print(f"\nWith seed {seed_val}:")
                print(f"  random.randint(1,100) → {random.randint(1,100)}")
                print(f"  random.random()       → {random.random():.6f}")
                print("Run again with same seed → same numbers!")
            else:
                print("Invalid seed – skipping demo.")

    print("\nThanks for playing! Randomness is fun — and powerful.")
    print("Remember: random is pseudo-random → use secrets module for security.\n")


if __name__ == "__main__":
    main()