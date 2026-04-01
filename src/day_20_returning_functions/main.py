# src/day_20_returning_functions/main.py
"""
Day 20: Returning Functions in Python – Interactive Explorer
Learn how to return values from functions, return multiple values, early returns, 
and the important difference between return vs print.
"""

def print_return_guide():
    print("\n" + "═" * 70)
    print("Returning Functions – Key Concepts (Day 20)")
    print("═" * 70)
    print("• return statement sends a value back to the caller")
    print("• Functions without return implicitly return None")
    print("• You can return multiple values (as a tuple)")
    print("• Early return exits the function immediately")
    print("• return vs print: print shows output, return passes data")
    print("• Returned values can be used in expressions, assigned, or passed to other functions")
    print("═" * 70)


def calculate_statistics(numbers: list) -> tuple:
    """Return multiple values: sum, average, min, max"""
    if not numbers:
        return 0, 0, 0, 0
    total = sum(numbers)
    avg = round(total / len(numbers), 2)
    minimum = min(numbers)
    maximum = max(numbers)
    return total, avg, minimum, maximum


def get_grade_with_feedback(score: float) -> tuple[str, str]:
    """Return both grade and feedback message"""
    if score >= 90:
        return "A+", "Excellent work!"
    elif score >= 80:
        return "A", "Very good!"
    elif score >= 70:
        return "B", "Good job!"
    elif score >= 60:
        return "C", "Satisfactory"
    elif score >= 50:
        return "D", "Needs improvement"
    else:
        return "F", "Please work harder"


def is_valid_password(password: str) -> tuple[bool, str]:
    """Return (is_valid, reason) - common pattern"""
    if len(password) < 8:
        return False, "Password too short (minimum 8 characters)"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    return True, "Strong password!"


def main():
    print("Welcome to Day 20 – Returning Functions!")
    print("Understand the power of return vs print with interactive examples.\n")

    print_return_guide()

    while True:
        print("\n" + "─" * 60)
        print("Choose a Returning Functions Demo:")
        print("  1) Return Multiple Values (Statistics)")
        print("  2) Grade with Feedback (Tuple Return)")
        print("  3) Password Validator (bool + message)")
        print("  4) Early Return Example")
        print("  5) Return vs Print Comparison")
        print("  6) Build Your Own Calculator Function")
        print("─" * 60)

        choice = input("→ ").strip().lower()

        if choice in ('quit', 'q', 'exit'):
            break

        try:
            if choice == "1":
                print("\nReturn Multiple Values")
                nums_str = input("Enter numbers separated by space: ")
                numbers = [float(x) for x in nums_str.split()]
                
                total, avg, min_val, max_val = calculate_statistics(numbers)
                
                print(f"\nResults:")
                print(f"  Sum      : {total}")
                print(f"  Average  : {avg}")
                print(f"  Minimum  : {min_val}")
                print(f"  Maximum  : {max_val}")

            elif choice == "2":
                print("\nGrade with Feedback")
                score = float(input("Enter your score (0-100): "))
                grade, feedback = get_grade_with_feedback(score)
                print(f"\nYour grade : {grade}")
                print(f"Feedback   : {feedback}")

            elif choice == "3":
                print("\nPassword Validator")
                pwd = input("Enter a password to check: ")
                is_valid, message = is_valid_password(pwd)
                if is_valid:
                    print("✅ Strong password!")
                else:
                    print(f"❌ {message}")

            elif choice == "4":
                print("\nEarly Return Example")
                num = int(input("Enter a number: "))
                def check_sign(n):
                    if n > 0:
                        return "Positive"
                    elif n < 0:
                        return "Negative"
                    else:
                        return "Zero"   # early return
                print(f"The number is {check_sign(num)}")

            elif choice == "5":
                print("\nReturn vs Print Comparison")
                def add_with_print(a, b):
                    print(a + b)   # only shows on screen
                
                def add_with_return(a, b):
                    return a + b   # can be used later
                
                x = 15
                y = 27
                
                print("Using print inside function:")
                add_with_print(x, y)
                
                print("\nUsing return:")
                result = add_with_return(x, y)
                print(f"Result = {result}")
                print(f"Result * 2 = {result * 2}")   # we can reuse the returned value!

            elif choice == "6":
                print("\nBuild Your Own Calculator Function")
                a = float(input("First number: "))
                b = float(input("Second number: "))
                op = input("Operator (+ - * /): ").strip()
                
                def calculate(x, y, operator):
                    if operator == "+":
                        return x + y
                    elif operator == "-":
                        return x - y
                    elif operator == "*":
                        return x * y
                    elif operator == "/":
                        if y == 0:
                            return "Error: Division by zero"
                        return x / y
                    else:
                        return "Invalid operator"
                
                result = calculate(a, b, op)
                print(f"Result: {result}")

            else:
                print("Please choose 1-6.")

        except ValueError:
            print("✗ Please enter valid numbers.")
        except Exception as e:
            print(f"✗ Error: {e}")

    print("\nFantastic! You now understand the importance of returning values from functions.")
    print("Remember: return passes data, print only displays it.")
    print("Next: Return vs Print deep dive (Day 21).\n")


if __name__ == "__main__":
    main()