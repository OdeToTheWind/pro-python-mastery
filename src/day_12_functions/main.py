# src/day_12_functions/main.py
"""
Day 12: Functions in Python – Interactive Explorer
Learn how to define, call, and use functions with parameters, return values, 
default arguments, *args, **kwargs, and docstrings.
"""

def greet_user(name: str, title: str = "friend") -> str:
    """Return a personalized greeting."""
    return f"Hello {title} {name}!"


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate Body Mass Index."""
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    return round(weight_kg / (height_m ** 2), 2)


def calculate_grade(score: float) -> str:
    """Return letter grade based on score."""
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"


def add_numbers(*args: float) -> float:
    """Add any number of numbers."""
    return sum(args)


def create_profile(**kwargs) -> dict:
    """Create a user profile from keyword arguments."""
    return kwargs


def print_cheat_sheet():
    print("\n" + "═" * 70)
    print("Functions in Python – Quick Reference (Day 12)")
    print("═" * 70)
    print("• def function_name(parameters):")
    print("• Parameters vs Arguments")
    print("• Default arguments (title='friend')")
    print("• *args   → variable number of positional arguments")
    print("• **kwargs → variable number of keyword arguments")
    print("• return statement (functions can return values or None)")
    print("• Docstrings → triple quotes for documentation")
    print("• Type hints (PEP 484) → name: type")
    print("═" * 70)


def main():
    print("Welcome to Day 12 – Functions in Python!")
    print("Let's explore how to write reusable, clean, and powerful functions.\n")

    print_cheat_sheet()

    while True:
        print("\n" + "─" * 60)
        print("Choose a function demo (or 'quit' to exit):")
        print("  1) Personalized Greeting")
        print("  2) BMI Calculator")
        print("  3) Grade Calculator")
        print("  4) Add Any Number of Numbers (*args)")
        print("  5) Create User Profile (**kwargs)")
        print("  6) Run All Demos")
        print("─" * 60)

        choice = input("→ ").strip()

        if choice.lower() in ('quit', 'q', 'exit'):
            break

        try:
            if choice == "1":
                name = input("Enter your name: ").strip()
                title = input("Enter title (e.g. Mr., Dr., or press Enter for default): ").strip()
                greeting = greet_user(name, title) if title else greet_user(name)
                print(f"\n{greeting}")

            elif choice == "2":
                weight = float(input("Enter weight (kg): "))
                height = float(input("Enter height (m): "))
                bmi = calculate_bmi(weight, height)
                print(f"\nYour BMI is: {bmi}")
                if bmi < 18.5:
                    print("Category: Underweight")
                elif bmi < 25:
                    print("Category: Normal weight")
                elif bmi < 30:
                    print("Category: Overweight")
                else:
                    print("Category: Obese")

            elif choice == "3":
                score = float(input("Enter your score (0-100): "))
                grade = calculate_grade(score)
                print(f"\nYour grade is: {grade}")

            elif choice == "4":
                print("Enter numbers separated by space (e.g. 10 20 30):")
                nums = list(map(float, input().split()))
                total = add_numbers(*nums)
                print(f"\nSum = {total}")

            elif choice == "5":
                print("Enter profile details (key=value format, one per line). Type 'done' when finished:")
                profile_data = {}
                while True:
                    line = input()
                    if line.lower() == 'done':
                        break
                    if '=' in line:
                        key, value = line.split('=', 1)
                        profile_data[key.strip()] = value.strip()
                profile = create_profile(**profile_data)
                print(f"\nCreated profile: {profile}")

            elif choice == "6":
                print("\nRunning all demos...")
                print(greet_user("Alex", "Mr."))
                print("BMI:", calculate_bmi(70, 1.75))
                print("Grade:", calculate_grade(85))
                print("Sum:", add_numbers(5, 10, 15, 20))
                print("Profile:", create_profile(name="Sara", age=28, city="Bengaluru"))

            else:
                print("Invalid choice. Please select 1-6.")

        except ValueError as e:
            print(f"✗ Input error: {e}")
        except Exception as e:
            print(f"✗ Unexpected error: {e}")

    print("\nGreat work on Functions!")
    print("You now understand parameters, return values, *args, **kwargs, and docstrings.\n")


if __name__ == "__main__":
    main()