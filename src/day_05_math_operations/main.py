# src/day_05_math_operations/main.py
"""
Day 5: Mathematical Operations in Python – Interactive Lesson
Covers: +, -, *, /, //, %, ** + precedence, user input, error handling
"""

def safe_float_input(prompt: str) -> float | None:
    """Get float from user with validation loop. Returns None if user wants to quit."""
    while True:
        value = input(prompt).strip()
        if value.lower() in ('quit', 'q', 'exit'):
            return None
        try:
            if not value:
                print("❌ Please enter a number (cannot be empty).")
                continue
            return float(value)
        except ValueError:
            print("❌ Invalid input — please enter a valid number.")


def explain_operators():
    print("\n" + "═" * 70)
    print("Python Arithmetic Operators – Quick Reference (Day 5)")
    print("═" * 70)
    print("Operator | Name              | Example     | Result    | Notes")
    print("─────────┼───────────────────┼─────────────┼───────────┼──────────────────────────────────")
    print("   +     │ Addition          │  5 + 3      │    8      │ ")
    print("   -     │ Subtraction       │  5 - 3      │    2      │ ")
    print("   *     │ Multiplication    │  5 * 3      │   15      │ ")
    print("   /     │ True Division     │  5 / 2      │   2.5     │ Always returns float")
    print("  //     │ Floor Division    │  5 // 2     │    2      │ Integer result, rounds down")
    print("   %     │ Modulus / Remainder│  5 % 2      │    1      │ Remainder after division")
    print("  **     │ Exponentiation    │  5 ** 2     │   25      │ Power (right-associative)")
    print("═" * 70)
    print("Important:")
    print("• Operator precedence: ** > * / // % > + -  (use () to control order)")
    print("• Division by zero → ZeroDivisionError (we'll handle it!)")


def perform_operation(a: float, b: float, op: str) -> tuple[float | str, str]:
    """Execute operation safely and return (result, description)"""
    if op == "+":
        return a + b, "Addition"
    if op == "-":
        return a - b, "Subtraction"
    if op == "*":
        return a * b, "Multiplication"
    if op == "/":
        if b == 0:
            return "Error", "Division by zero is not allowed"
        return a / b, "True Division (float result)"
    if op == "//":
        if b == 0:
            return "Error", "Division by zero is not allowed"
        return a // b, "Floor Division (integer result)"
    if op == "%":
        if b == 0:
            return "Error", "Division by zero is not allowed"
        return a % b, "Modulus (remainder)"
    if op == "**":
        return a ** b, "Exponentiation (power)"
    return "Unknown", "Invalid operator"


def main():
    print("Welcome to Day 5 – Mathematical Operations (Interactive!)")
    print("We'll explore all basic arithmetic operators with YOUR numbers.\n")

    explain_operators()

    while True:
        print("\n" + "─" * 60)
        print("Enter two numbers and an operator (or type 'quit' to exit)")
        print("Operators: +  -  *  /  //  %  **")
        print("─" * 60)

        num1 = safe_float_input("First number  → ")
        if num1 is None:
            break

        op_input = input("Operator (+ - * / // % **) → ").strip()
        if op_input.lower() in ("quit", "q", "exit"):
            break
        if op_input not in ["+", "-", "*", "/", "//", "%", "**"]:
            print("❌ Invalid operator. Please use one of: + - * / // % **")
            continue

        num2 = safe_float_input("Second number → ")
        if num2 is None:
            break

        result, description = perform_operation(num1, num2, op_input)

        if result == "Error":
            print(f"✗ {description}")
        else:
            display_result = int(result) if isinstance(result, float) and result.is_integer() else result
            print(f"✓ {num1} {op_input} {num2} = {display_result}")
            print(f"   → {description}")

        # Bonus: show equivalent with parentheses for precedence demo
        if op_input in ["+", "-", "*"]:
            if op_input == "+":
                expr = num1 + num2
            elif op_input == "-":
                expr = num1 - num2
            else:
                expr = num1 * num2
            print(f"   (Try: ({num1} {op_input} {num2}) * 2 → {expr * 2})")

    print("\nGreat session! You now know Python's arithmetic operators.")
    print("Remember: / always gives float, // gives integer division, % for remainders, ** for powers.\n")


if __name__ == "__main__":
    main()