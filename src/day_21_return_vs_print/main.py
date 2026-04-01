# src/day_21_return_vs_print/main.py
"""
Day 21: Return vs Print – Interactive Explorer
Understand the crucial difference between returning a value and printing it.
"""

def print_vs_return_guide():
    print("\n" + "═" * 70)
    print("Return vs Print – Core Concepts (Day 21)")
    print("═" * 70)
    print("• print() → Displays output on the screen (side effect)")
    print("• return → Sends a value back to the caller (data passing)")
    print("• You can use returned values in expressions, assignments, or pass them to other functions")
    print("• print() inside a function usually makes the function less reusable")
    print("• Good functions generally return values instead of printing them")
    print("═" * 70)


def add_print_only(a: float, b: float):
    """This function only prints — cannot be reused easily"""
    print(a + b)


def add_with_return(a: float, b: float) -> float:
    """This function returns the result — very reusable"""
    return a + b


def calculate_final_price(base_price: float, tax_rate: float = 0.18) -> float:
    """Realistic example: returns value for further calculation"""
    tax = base_price * tax_rate
    final = base_price + tax
    return round(final, 2)


def main():
    print("Welcome to Day 21 – Return vs Print!")
    print("This is one of the most important concepts for writing good Python code.\n")

    print_vs_return_guide()

    while True:
        print("\n" + "─" * 60)
        print("Choose a Demo to Understand Return vs Print:")
        print("  1) Basic Return vs Print Comparison")
        print("  2) Reusability Example (Calculator)")
        print("  3) Real-world: Price Calculator with Tax")
        print("  4) Function Composition (Chaining returned values)")
        print("  5) Common Mistake: Printing Instead of Returning")
        print("  6) When to Use Print vs Return")
        print("─" * 60)

        choice = input("→ ").strip().lower()

        if choice in ('quit', 'q', 'exit'):
            break

        try:
            if choice == "1":
                print("\nBasic Comparison")
                print("Using print inside function:")
                add_print_only(15, 27)

                print("\nUsing return:")
                result = add_with_return(15, 27)
                print(f"Returned value: {result}")
                print(f"Result * 2 = {result * 2}")
                print(f"Result + 100 = {result + 100}")

            elif choice == "2":
                print("\nReusability Example")
                x = float(input("Enter first number: "))
                y = float(input("Enter second number: "))

                print("Bad way (print inside):")
                add_print_only(x, y)

                print("\nGood way (return):")
                res = add_with_return(x, y)
                print(f"Sum is {res}")
                print(f"Sum squared is {res ** 2}")

            elif choice == "3":
                print("\nReal-world: Price Calculator")
                base = float(input("Enter base price (₹): "))
                final_price = calculate_final_price(base)

                print(f"Base Price     : ₹{base}")
                print(f"Final Price (incl. 18% tax): ₹{final_price}")

                discount = float(input("Enter discount percentage: ") or 0)
                discounted = final_price * (1 - discount/100)
                print(f"After {discount}% discount: ₹{round(discounted, 2)}")

            elif choice == "4":
                print("\nFunction Composition (Chaining)")
                nums = [10, 20, 30, 40]
                
                def get_average(lst):
                    return sum(lst) / len(lst)
                
                def format_result(value):
                    return f"Average = {value:.2f}"
                
                avg = get_average(nums)
                message = format_result(avg)
                print(message)

            elif choice == "5":
                print("\nCommon Mistake: Printing Instead of Returning")
                print("Imagine you have a function that calculates tax...")
                
                def bad_tax_calculator(price):
                    print(price * 0.18)   # Common beginner mistake
                
                def good_tax_calculator(price):
                    return price * 0.18
                
                price = 1000
                print("Bad function (only prints):")
                bad_tax_calculator(price)
                
                print("\nGood function (returns value):")
                tax = good_tax_calculator(price)
                print(f"Tax amount: ₹{tax}")
                print(f"Total with tax: ₹{price + tax}")

            elif choice == "6":
                print("\nWhen to Use Print vs Return")
                print("Use PRINT when:")
                print("• You want to show information to the user")
                print("• Debugging / logging")
                print("• Creating CLI output")
                print("")
                print("Use RETURN when:")
                print("• You want to use the result later")
                print("• Building reusable functions")
                print("• Function composition")
                print("• Testing and validation")

            else:
                print("Please choose 1-6.")

        except ValueError:
            print("✗ Please enter valid numbers.")
        except Exception as e:
            print(f"✗ Error: {e}")

    print("\nWell done! You now clearly understand Return vs Print.")
    print("This distinction is critical for writing clean, reusable, and professional Python code.")
    print("Next: Docstrings vs Comments (Day 22).\n")


if __name__ == "__main__":
    main()