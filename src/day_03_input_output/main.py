"""
Day 03: Input and Print Functions - Interactive User Profile Builder
Focus: input(), print() with advanced formatting, type conversion, validation, and user-friendly console interaction.
"""

def get_validated_input(prompt: str, expected_type: type = str, min_value: float | None = None) -> str | int | float:
    """
    Helper to get input with validation and type conversion.
    Retries until valid input is provided.
    """
    while True:
        try:
            value = input(prompt).strip()
            if not value:
                print("Input cannot be empty. Please try again.")
                continue

            converted = expected_type(value)

            if min_value is not None and converted < min_value:
                print(f"Value must be at least {min_value}. Please try again.")
                continue

            return converted
        except ValueError:
            print(f"Invalid input. Please enter a valid {expected_type.__name__}.")
        except Exception as e:
            print(f"Unexpected error: {e}. Please try again.")


def build_user_profile() -> dict:
    """Collect and validate user information interactively."""
    print("\n" + "=" * 40)
    print("   WELCOME TO PROFILE BUILDER (Day 03)")
    print("=" * 40)

    name = get_validated_input("Enter your full name: ", str)
    age = get_validated_input("Enter your age: ", int, min_value=0)
    height_cm = get_validated_input("Enter your height in cm: ", float, min_value=50.0)
    hobby = get_validated_input("Enter your favorite hobby: ", str)

    return {
        "name": name,
        "age": age,
        "height_cm": height_cm,
        "hobby": hobby,
    }


def print_profile(profile: dict) -> None:
    """Display the profile in a clean, formatted way using advanced print features."""
    print("\n" + "-" * 50)
    print(f"{' USER PROFILE SUMMARY ':^50}")
    print("-" * 50)

    # Using f-strings with alignment, precision, and expressions
    print(f"Name          : {profile['name']:<30}")
    print(f"Age           : {profile['age']:>3} years old")
    print(f"Height        : {profile['height_cm']:>6.1f} cm")
    print(f"Hobby         : {profile['hobby'].title():<30}")

    # Fun dynamic message with conditional formatting
    status = "experienced" if profile["age"] >= 25 else "young"
    print(f"\nHello {profile['name'].split()[0]}! As a {status} {profile['hobby'].lower()} enthusiast,")
    print(f"you're {2026 - profile['age'] + 18:+d} years from turning 18 again! 🎉")

    print("-" * 50)


def run_interactive_demo() -> None:
    """Main entry point: Build and display profile interactively."""
    profile = build_user_profile()
    print_profile(profile)


if __name__ == "__main__":
    run_interactive_demo()