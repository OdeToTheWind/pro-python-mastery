# src/day_17_positional_keyword_arguments/main.py
"""
Day 17: Positional and Keyword Arguments – Interactive Explorer
Master how to pass arguments to functions using positional, keyword, default, *args, and **kwargs.
"""

def print_arguments_guide():
    print("\n" + "═" * 70)
    print("Positional vs Keyword Arguments – Quick Reference (Day 17)")
    print("═" * 70)
    print("• Positional arguments: passed by position/order")
    print("• Keyword arguments: passed by name (order doesn't matter)")
    print("• Default arguments: have fallback values")
    print("• *args   → collects extra positional arguments as tuple")
    print("• **kwargs → collects extra keyword arguments as dictionary")
    print("")
    print("Rules:")
    print("1. Positional arguments must come before keyword arguments")
    print("2. *args must come before **kwargs")
    print("3. Default parameters must come after non-default ones")
    print("═" * 70)


def student_info(name: str, age: int, grade: str = "10th", city: str = "Unknown") -> str:
    """Demonstrates default + keyword arguments"""
    return f"Student: {name}, Age: {age}, Grade: {grade}, City: {city}"


def calculate_total(*items: float) -> float:
    """Demonstrates *args"""
    return sum(items)


def create_order(customer: str, **details) -> dict:
    """Demonstrates **kwargs"""
    order = {"customer": customer}
    order.update(details)
    return order


def flexible_greeting(greeting: str = "Hello", *names, **styles):
    """Advanced example combining all argument types"""
    result = []
    for name in names:
        styled = styles.get(name.lower(), "")
        result.append(f"{greeting} {styled} {name}!")
    return "\n".join(result) if result else f"{greeting} everyone!"


def main():
    print("Welcome to Day 17 – Positional and Keyword Arguments!")
    print("Learn how to call functions flexibly and professionally.\n")

    print_arguments_guide()

    while True:
        print("\n" + "─" * 60)
        print("Choose a Demo (or 'quit' to exit):")
        print("  1) Keyword vs Positional Arguments")
        print("  2) Default Arguments")
        print("  3) *args – Variable Positional Arguments")
        print("  4) **kwargs – Variable Keyword Arguments")
        print("  5) Mixed Arguments (All Together)")
        print("  6) Real-world Example: Student Registration")
        print("─" * 60)

        choice = input("→ ").strip().lower()

        if choice in ('quit', 'q', 'exit'):
            break

        try:
            if choice == "1":
                print("\nKeyword vs Positional:")
                # Positional
                print(student_info("Rahul", 16))
                # Keyword (order doesn't matter)
                print(student_info(age=17, name="Priya", city="Mumbai"))

            elif choice == "2":
                print("\nDefault Arguments:")
                print(student_info("Anika", 15))                    # uses defaults
                print(student_info("Vikram", 18, grade="12th"))     # overrides grade

            elif choice == "3":
                print("\n*args Example:")
                total1 = calculate_total(100, 250, 75)
                total2 = calculate_total(500, 1200, 300, 450)
                print(f"Total 1: ₹{total1}")
                print(f"Total 2: ₹{total2}")

            elif choice == "4":
                print("\n**kwargs Example:")
                order = create_order("Alice", item="Laptop", price=65000, quantity=1, discount=10)
                print("Order details:")
                for key, value in order.items():
                    print(f"  {key:12} : {value}")

            elif choice == "5":
                print("\nMixed Arguments (*args + **kwargs):")
                message = flexible_greeting(
                    "Namaste",
                    "Aarav", "Diya", "Rohan",
                    aarav="ji",
                    diya="ji",
                    rohan=""
                )
                print(message)

            elif choice == "6":
                print("\nStudent Registration System")
                name = input("Student Name: ").strip()
                age = int(input("Age: "))
                grade = input("Grade (press Enter for default '10th'): ").strip() or "10th"
                city = input("City (press Enter for default): ").strip() or "Bengaluru"
                
                # Using keyword arguments for clarity
                info = student_info(name=name, age=age, grade=grade, city=city)
                print("\n" + info)

            else:
                print("Please choose 1-6.")

        except ValueError:
            print("✗ Please enter valid numbers where required.")
        except Exception as e:
            print(f"✗ Error: {e}")

    print("\nExcellent! You now understand how to use arguments flexibly in Python.")
    print("This knowledge is essential for writing clean, reusable functions.")
    print("Next: Python Dictionaries and Lists (Day 18).\n")


if __name__ == "__main__":
    main()