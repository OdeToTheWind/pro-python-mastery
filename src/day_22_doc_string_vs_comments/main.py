# src/day_22_doc_string_vs_comments/main.py
"""
Day 22: Docstrings vs Comments – Interactive Explorer
Learn the difference between comments (#) and docstrings (" " "), and why docstrings matter.
"""

def print_guide():
    print("\n" + "═" * 70)
    print("Docstrings vs Comments – Quick Reference (Day 22)")
    print("═" * 70)
    print("Comments (#):")
    print("• For developers reading the code")
    print("• Ignored by Python and documentation tools")
    print("• Use for 'why' and temporary notes")
    print("")
    print("Docstrings (triple quotes):")
    print("• For users and tools (help(), Sphinx, IDEs)")
    print("• Attached to modules, classes, and functions as __doc__")
    print("• Can be accessed at runtime")
    print("• Standard formats: Google, NumPy, reStructuredText")
    print("═" * 70)


def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers and return the result.
    
    This is a proper docstring using Google style.
    
    Args:
        a (int): The first number
        b (int): The second number
        
    Returns:
        int: The sum of a and b
    """
    # This is a comment - explains "how" or "why" internally
    # We could add validation here in the future
    return a + b


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate Body Mass Index (BMI).
    
    A simple one-line docstring is also acceptable for short functions.
    
    Args:
        weight_kg (float): Weight in kilograms
        height_m (float): Height in meters
        
    Returns:
        float: BMI value rounded to 2 decimal places
    """
    if height_m <= 0:
        raise ValueError("Height must be positive")
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def main():
    print("Welcome to Day 22 – Docstrings vs Comments!")
    print("Learn how to write proper documentation for your code.\n")

    print_guide()

    while True:
        print("\n" + "─" * 60)
        print("Choose a Demo:")
        print("  1) See Docstring vs Comment in Action")
        print("  2) Interactive Function Documentation")
        print("  3) Help() Simulation")
        print("  4) Build a Function with Proper Docstring")
        print("  5) Common Documentation Mistakes")
        print("─" * 60)

        choice = input("→ ").strip().lower()

        if choice in ('quit', 'q', 'exit'):
            break

        try:
            if choice == "1":
                print("\nFunction with both docstring and comments:")
                print("Docstring (accessible via help()):")
                print(add_numbers.__doc__)
                
                print("\nInternal comments (not accessible):")
                print("   # These are ignored by help() and documentation tools")

            elif choice == "2":
                print("\nInteractive Documentation")
                weight = float(input("Enter weight (kg): "))
                height = float(input("Enter height (m): "))
                
                bmi = calculate_bmi(weight, height)
                print(f"\nYour BMI is: {bmi}")
                
                print("\nFunction docstring:")
                print(calculate_bmi.__doc__)

            elif choice == "3":
                print("\nSimulating help() on our functions:")
                print("=== help(add_numbers) ===")
                print(add_numbers.__doc__)
                print("\n=== help(calculate_bmi) ===")
                print(calculate_bmi.__doc__)

            elif choice == "4":
                print("\nCreate your own function with proper docstring")
                print("Example structure:")
                print('def your_function(param1, param2):')
                print('    """')
                print('    Short description.')
                print('')
                print('    Args:')
                print('        param1: description')
                print('    Returns:')
                print('        description')
                print('    """')
                print("\nTry writing one mentally and imagine using help(your_function)")

            elif choice == "5":
                print("\nCommon Documentation Mistakes:")
                print("• Writing comments instead of docstrings for public functions")
                print("• No docstring at all")
                print("• Outdated docstrings after changing function")
                print("• Using print() for documentation instead of proper docstrings")
                print("• Poor or missing argument descriptions")

            else:
                print("Please choose 1-5.")

        except ValueError:
            print("✗ Please enter valid numbers.")
        except Exception as e:
            print(f"✗ Error: {e}")

    print("\nGreat work! You now understand the importance of proper documentation.")
    print("Well-written docstrings make your code professional and maintainable.")
    print("Next: Scope and Local/Global Variables (Day 23).\n")


if __name__ == "__main__":
    main()