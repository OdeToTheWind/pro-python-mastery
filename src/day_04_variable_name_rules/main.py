# src/day_04_variable_name_rules/main.py
"""
Day 4: Variable Naming Rules – Interactive Lesson
Focus: Rules + PEP 8 style + Descriptive names
"""

def is_valid_variable_name(name: str) -> tuple[bool, str]:
    """Return (is_valid, reason)"""
    if not name:
        return False, "Name cannot be empty"

    if name[0].isdigit():
        return False, "Cannot start with a digit"

    if not (name[0].isalpha() or name[0] == "_"):
        return False, "Must start with letter or underscore"

    for char in name[1:]:
        if not (char.isalnum() or char == "_"):
            return False, "Only letters, digits, underscores allowed"

    import keyword
    if keyword.iskeyword(name):
        return False, f"'{name}' is a Python keyword"

    return True, "Valid syntax"


def print_naming_tips():
    print("\n" + "═" * 60)
    print("PEP 8 – Variable Naming Style Recommendations (Professional Python)")
    print("═" * 60)
    print("• Use snake_case → lowercase_with_underscores")
    print("• Make names descriptive: user_age → better than x or a")
    print("• Avoid single-letter names (except in very short loops: i, j, k)")
    print("• Don't use: l, O, I  (look like 1 and 0)")
    print("• Constants: ALL_CAPS_WITH_UNDERSCORES")
    print("• Never override built-ins: list, str, dict, max, min, sum, ...")
    print("• Private-ish variables: _single_leading_underscore (convention)")
    print("═" * 60)


def main():
    print("Welcome to Day 4 – Variable Naming Rules (Interactive!)")
    print("We'll check syntax rules + discuss good style.\n")

    print_naming_tips()

    examples = [
        "age",
        "user_name",
        "totalPrice",
        "2fast",
        "my-name",
        "class",
        "PI_VALUE",
        "_hidden",
        "for",
        "very_long_and_clear_variable_name_2025",
        "l",           # bad – looks like 1
        "O",           # bad – looks like 0
        "max",         # shadows built-in
    ]

    print("\nQuick syntax check on some names:")
    for name in examples:
        valid, reason = is_valid_variable_name(name)
        mark = "✅" if valid else "❌"
        print(f"{mark}  {name:28} → {reason}")

    # ── Interactive part ───────────────────────────────────────────────
    print("\n" + "─" * 50)
    print("Now YOU try! Enter variable names (or type 'quit' to finish)")
    print("─" * 50)

    while True:
        user_input = input("\nYour variable name → ").strip()

        if user_input.lower() in ("quit", "exit", "q"):
            break

        valid, reason = is_valid_variable_name(user_input)

        if valid:
            print("✓ Valid syntax!")
            if "_" not in user_input and len(user_input) > 8:
                print("  (Tip: consider snake_case for multi-word names)")
            if user_input.isupper():
                print("  (Looks like a constant — good if it really is!)")
            if user_input.startswith("_"):
                print("  (Leading underscore → usually means private / internal)")
        else:
            print(f"✗ Invalid: {reason}")

        # Mini style suggestion
        if valid and " " not in user_input:
            suggested = user_input.replace(" ", "_").lower()
            if suggested != user_input:
                print(f"  Style tip: maybe → {suggested}")

    print("\nGreat work! Day 4 complete.")
    print("Remember: syntax = what Python allows")
    print("          style   = what humans read easily → follow PEP 8\n")


if __name__ == "__main__":
    main()