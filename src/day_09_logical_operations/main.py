# src/day_09_logical_operations/main.py
"""
Day 9: Logical Operations – and, or, not
Interactive explorer with truth table, short-circuit demo, and real-world decisions.
"""

def get_yes_no(prompt: str) -> bool | None:
    """Get yes/no answer with quit support"""
    while True:
        ans = input(prompt).strip().lower()
        if ans in ('quit', 'q', 'exit'):
            return None
        if ans in ('y', 'yes', '1', 'true'):
            return True
        if ans in ('n', 'no', '0', 'false'):
            return False
        print("Please answer yes/y or no/n")


def get_number(prompt: str, allow_float: bool = False) -> float | int | None:
    """Get number (int or float) with quit support"""
    while True:
        val = input(prompt).strip()
        if val.lower() in ('quit', 'q', 'exit'):
            return None
        try:
            if allow_float:
                return float(val)
            return int(val)
        except ValueError:
            print("Please enter a valid number.")


def print_truth_table():
    print("\n" + "═" * 70)
    print("Python Logical Operators – Truth Table")
    print("═" * 70)
    print("   A      B     A and B    A or B     not A     not B")
    print("───┼──────┼─────────┼──────────┼───────────┼──────────")
    values = [False, True]
    for a in values:
        for b in values:
            print(f" {str(a):<5} {str(b):<5} {str(a and b):<9} {str(a or b):<9} {str(not a):<9} {str(not b)}")
    print("\nKey points:")
    print("• and → True only if BOTH are True")
    print("• or  → True if AT LEAST ONE is True")
    print("• not → reverses the value")
    print("• Short-circuit: and stops on first False, or stops on first True")
    print("• Truthy: non-zero, non-empty, True")
    print("• Falsy: 0, 0.0, '', [], {}, None, False")
    print("═" * 70)


def check_access(age: int, has_ticket: bool, is_vip: bool, has_coupon: bool) -> str:
    """Example of combining logical operators in real decision"""
    if age >= 18 and has_ticket:
        if is_vip or has_coupon:
            return "VIP / Discount Entry → Welcome to premium area!"
        else:
            return "Regular Adult Entry → Enjoy the event!"
    elif age >= 13 and has_ticket:
        return "Student/Teen Entry → Limited access area"
    elif age < 13 and has_ticket and has_coupon:
        return "Child with coupon → Special family entry"
    else:
        return "Access Denied – check age, ticket, or coupon requirements"


def main():
    print("Welcome to Day 9 – Logical Operators (and / or / not)")
    print("We'll explore truth tables, short-circuiting, and combined decisions.\n")

    print_truth_table()

    while True:
        print("\n" + "─" * 60)
        print("Scenario: Concert / Event Access Checker")
        print("Answer the questions below (type 'quit' to exit)")
        print("─" * 60)

        age = get_number("Your age: ")
        if age is None:
            break

        has_ticket = get_yes_no("Do you have a valid ticket? (y/n): ")
        if has_ticket is None:
            break

        is_vip = get_yes_no("Are you a VIP member? (y/n): ")
        if is_vip is None:
            break

        has_coupon = get_yes_no("Do you have a discount coupon? (y/n): ")
        if has_coupon is None:
            break

        decision = check_access(int(age), has_ticket, is_vip, has_coupon)
        print(f"\n→ Final decision: {decision}")

        # Short-circuit behavior demonstration
        print("\nShort-circuit examples (observe what gets printed):")
        print("  First example: age >= 18 and print('Checking ticket...')")
        if age >= 18 and print("  → Checking ticket..."):
            print("  → Ticket check passed (this line only runs if age >= 18)")
        else:
            print("  → Age condition failed → ticket check skipped")

        print("\n  Second example: has_ticket or print('No ticket → asking for coupon')")
        if has_ticket or print("  → No ticket → asking for coupon"):
            print("  → Access possible (short-circuited if has_ticket is True)")
        else:
            print("  → No ticket and no coupon path taken")

        print("\nTry different combinations to see how 'and' and 'or' behave!")

    print("\nGreat session! You now understand logical operators and short-circuit evaluation.")
    print("Next topic preview: while and for loops.\n")


if __name__ == "__main__":
    main()