# src/day_08_if_else_conditionals/main.py
"""
Day 8: If / Elif / Else Conditionals – Interactive Decision Maker
Ask user questions → make decisions → give personalized output
"""

def safe_int_input(prompt: str, min_val: int | None = None, max_val: int | None = None) -> int | None:
    """Get integer with validation + quit support"""
    while True:
        value = input(prompt).strip()
        if value.lower() in ('quit', 'q', 'exit'):
            return None
        try:
            num = int(value)
            if min_val is not None and num < min_val:
                print(f"❌ Must be at least {min_val}")
                continue
            if max_val is not None and num > max_val:
                print(f"❌ Must be at most {max_val}")
                continue
            return num
        except ValueError:
            print("❌ Please enter a valid integer.")


def safe_float_input(prompt: str) -> float | None:
    while True:
        value = input(prompt).strip()
        if value.lower() in ('quit', 'q', 'exit'):
            return None
        try:
            return float(value)
        except ValueError:
            print("❌ Please enter a valid number.")


def get_yes_no(prompt: str) -> bool | None:
    while True:
        ans = input(prompt).strip().lower()
        if ans in ('quit', 'q', 'exit'):
            return None
        if ans in ('y', 'yes'):
            return True
        if ans in ('n', 'no'):
            return False
        print("Please answer Y/yes or N/no.")


def explain_conditionals():
    print("\n" + "═" * 70)
    print("Python Conditional Statements Quick Guide (Day 8)")
    print("═" * 70)
    print("if condition:          → execute if True")
    print("elif other_condition:  → check only if previous was False")
    print("else:                  → run if all above were False")
    print("")
    print("Comparisons: == != > < >= <=")
    print("Logical: and or not")
    print("Truthy values: non-zero numbers, non-empty strings/lists, True")
    print("Falsy: 0, 0.0, '', [], {}, None, False")
    print("═" * 70)


def main():
    print("Welcome to Day 8 – If / Elif / Else Conditionals Explorer!")
    print("Answer a few questions — I'll make decisions for you.\n")

    explain_conditionals()

    while True:
        print("\n" + "─" * 60)
        print("Let's start! (type 'quit' at any prompt to exit)")
        print("─" * 60)

        age = safe_int_input("Your age: ", min_val=0, max_val=120)
        if age is None:
            break

        # Nested + chained example
        if age < 0:
            print("✗ You haven't been born yet?")
            continue
        elif age < 13:
            stage = "Child"
        elif age < 18:
            stage = "Teen"
        elif age < 65:
            stage = "Adult"
        else:
            stage = "Senior"

        print(f"→ You are classified as: {stage}")

        # Score / grade example
        score = safe_float_input("Your latest test score (0–100): ")
        if score is None:
            break

        if score < 0 or score > 100:
            print("❌ Score must be between 0 and 100. Skipping grade.")
            grade = "Invalid"
        elif score >= 90:
            grade = "A+ / Excellent"
        elif score >= 80:
            grade = "A / Very Good"
        elif score >= 70:
            grade = "B / Good"
        elif score >= 60:
            grade = "C / Average"
        elif score >= 50:
            grade = "D / Pass"
        else:
            grade = "F / Needs improvement"

        print(f"→ Your grade: {grade}")

        # Combined conditions example
        has_money = get_yes_no("Do you have money to spend today? (Y/N): ")
        if has_money is None:
            break

        likes_outdoor = get_yes_no("Do you like outdoor activities? (Y/N): ")
        if likes_outdoor is None:
            break

        if has_money and likes_outdoor:
            suggestion = "Go to a park / adventure activity / cafe with friends!"
        elif has_money and not likes_outdoor:
            suggestion = "Movie, shopping, or restaurant — indoor fun!"
        elif not has_money and likes_outdoor:
            suggestion = "Free walk in park, cycling, or people-watching."
        else:
            suggestion = "Netflix / reading / rest at home — recharge day!"

        print(f"→ Today's best activity suggestion: {suggestion}")

        # Bonus truthy/falsy demo
        name = input("Your name (just press Enter to skip): ").strip()
                # Personalized summary + feedback on empty name
        if name:
            print(f"\n→ Hello {name}! You are {age} years old ({stage}), "
                  f"scored {score} ({grade}), "
                  f"and today I suggest: {suggestion}")
            print("  Have a nice day!\n")
        else:
            print("\n→ You didn't enter a name.")
            print("  You can press Enter to skip, or type 'quit' to exit the program.")
            print(f"\n→ Hello anonymous explorer ! You are {age} years old ({stage}), "
                  f"scored {score} ({grade}), "
                  f"and today I suggest: {suggestion}")
            print("  Have a nice day anyway!\n")

        print("\nTry different answers to see how conditions change the outcome!")

    print("\nGreat session! You now understand how programs make decisions.")
    print("Remember: conditions → indentation matters → test edge cases.\n")


if __name__ == "__main__":
    main()