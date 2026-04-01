# src/day_15_while_loops/main.py
"""
Day 15: While Loops in Python – Interactive Explorer
Learn while loops, break, continue, while-else, and real-world input validation patterns.
"""

def print_while_cheat_sheet():
    print("\n" + "═" * 70)
    print("While Loops in Python – Quick Reference (Day 15)")
    print("═" * 70)
    print("while condition:")
    print("    # code block (must be indented)")
    print("")
    print("Key keywords:")
    print("• break    → exit the loop immediately")
    print("• continue → skip the rest of the current iteration")
    print("• while-else → else runs only if loop ended normally (no break)")
    print("")
    print("Common use cases:")
    print("• Input validation until correct data is entered")
    print("• Games (keep playing until user quits)")
    print("• Waiting for a condition (e.g. until balance > 0)")
    print("═" * 70)


def main():
    print("Welcome to Day 15 – While Loops in Python!")
    print("While loops are perfect for repeating until a condition changes.\n")

    print_while_cheat_sheet()

    while True:
        print("\n" + "─" * 60)
        print("Choose a While Loop Demo (or 'quit' to exit):")
        print("  1) Number Guessing Game")
        print("  2) Password Retry System (with limited attempts)")
        print("  3) Interactive Calculator (keep calculating until quit)")
        print("  4) Input Validation (force valid input)")
        print("  5) Countdown Timer Simulation")
        print("  6) while-else demonstration")
        print("─" * 60)

        choice = input("→ ").strip().lower()

        if choice in ('quit', 'q', 'exit'):
            print("Thank you for exploring While Loops!")
            break

        try:
            if choice == "1":
                print("\n🎮 Number Guessing Game")
                secret = 42  # Fixed for demo (in real games use random)
                attempts = 0
                max_attempts = 7

                while attempts < max_attempts:
                    guess = int(input(f"Attempt {attempts+1}/{max_attempts} - Guess the number (1-100): "))
                    attempts += 1

                    if guess == secret:
                        print(f"🎉 Correct! You guessed it in {attempts} attempts!")
                        break
                    elif guess < secret:
                        print("Too low! Try higher.")
                    else:
                        print("Too high! Try lower.")
                else:
                    print(f"Game over! The number was {secret}.")

            elif choice == "2":
                print("\n🔐 Password Retry System")
                correct_password = "python123"
                attempts = 0
                max_attempts = 3

                while attempts < max_attempts:
                    pwd = input("Enter password: ")
                    attempts += 1

                    if pwd == correct_password:
                        print("✅ Access granted! Welcome.")
                        break
                    else:
                        print(f"❌ Wrong password. {max_attempts - attempts} attempts left.")
                else:
                    print("❌ Too many failed attempts. Account locked.")

            elif choice == "3":
                print("\n🧮 Interactive Calculator (type 'quit' to stop)")
                while True:
                    expr = input("Enter expression (e.g. 12 + 34) or 'quit': ").strip()
                    if expr.lower() in ('quit', 'q', 'exit'):
                        break
                    try:
                        result = eval(expr, {"__builtins__": {}}, {})
                        print(f"Result: {result}")
                    except:
                        print("Invalid expression. Try again.")

            elif choice == "4":
                print("\nInput Validation Example")
                while True:
                    age_str = input("Enter your age (must be between 0 and 120): ")
                    if age_str.lower() in ('quit', 'q'):
                        break
                    try:
                        age = int(age_str)
                        if 0 <= age <= 120:
                            print(f"Valid age: {age}")
                            break
                        else:
                            print("Age must be between 0 and 120.")
                    except ValueError:
                        print("Please enter a valid number.")

            elif choice == "5":
                print("\nCountdown Timer Simulation")
                count = int(input("Enter countdown start number: ") or 10)
                while count > 0:
                    print(f"⏳ {count}...")
                    count -= 1
                print("🚀 Blast off!")

            elif choice == "6":
                print("\nwhile-else Demonstration")
                print("We'll search for a number. If found with break, else won't run.")
                target = int(input("Enter a number to search (1-10): ") or 5)
                i = 1
                while i <= 10:
                    if i == target:
                        print(f"Found {target} at position {i}!")
                        break
                    i += 1
                else:
                    print(f"Number {target} was not found in 1 to 10.")

            else:
                print("Invalid choice. Please select 1-6.")

        except ValueError:
            print("✗ Please enter a valid number.")
        except Exception as e:
            print(f"✗ Error: {e}")

    print("\nExcellent work! While loops are now clear.")
    print("Remember: Use while when you don't know in advance how many iterations you need.\n")


if __name__ == "__main__":
    main()