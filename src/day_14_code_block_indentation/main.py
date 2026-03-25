# src/day_14_code_block_indentation/main.py
"""
Day 14: Code Blocks and Indentation in Python – Interactive Explorer
Understand why indentation matters, common mistakes, and best practices.
"""

def print_indentation_guide():
    print("\n" + "═" * 70)
    print("Code Blocks & Indentation in Python (Day 14)")
    print("═" * 70)
    print("• Python uses indentation (not braces {}) to define code blocks")
    print("• Standard is 4 spaces (never mix tabs and spaces)")
    print("• Consistent indentation is mandatory")
    print("• Common errors: IndentationError, unexpected indent, unindent does not match")
    print("• Blocks occur after:, if, for, while, def, with, try, class, etc.")
    print("═" * 70)
    print("Rule: All statements in the same block must have the same indentation level.")
    print("═" * 70)


def demonstrate_indentation():
    print("\nLet's see correct vs incorrect indentation through examples.\n")

    print("Example 1: Correct if-else block")
    score = 85
    if score >= 90:
        print("   Grade: A+")
    elif score >= 80:
        print("   Grade: A")
    else:
        print("   Grade: B")
    print("   → This block ends here\n")

    print("Example 2: Correct for loop")
    for i in range(3):
        print(f"   Iteration {i + 1}")
        print("   Inside the loop")
    print("   → Loop block ended\n")


def main():
    print("Welcome to Day 14 – Code Blocks and Indentation")
    print("The most important (and sometimes tricky) concept in Python!\n")

    print_indentation_guide()
    demonstrate_indentation()

    while True:
        print("\n" + "─" * 60)
        print("Choose an activity to practice indentation:")
        print("  1) Fix broken code (IndentationError examples)")
        print("  2) Build a simple menu with proper blocks")
        print("  3) Nested blocks challenge (if inside for)")
        print("  4) Create your own function with correct indentation")
        print("  5) Common mistakes quiz")
        print("─" * 60)

        choice = input("→ ").strip()

        if choice.lower() in ('quit', 'q', 'exit'):
            break

        try:
            if choice == "1":
                print("\nFix this broken code mentally:")
                print("if x > 10:")
                print("print('Greater than 10')   # ← Wrong indentation")
                print("    print('Still inside?') # ← Mixed levels")
                fixed = input("\nWhat would the correct version look like? (describe or skip): ")
                print("Correct version uses consistent 4 spaces for each block.")

            elif choice == "2":
                print("\nBuilding a proper menu with indentation:")
                print("Main block starts here")
                option = input("Choose 1, 2 or 3: ").strip()
                
                if option == "1":
                    print("    You chose option 1")
                    for i in range(3):
                        print(f"        Sub-step {i+1} inside option 1")
                elif option == "2":
                    print("    You chose option 2")
                    if True:                     # nested if
                        print("        This is nested inside option 2")
                else:
                    print("    You chose option 3")
                print("Back to main block after the if-elif-else")

            elif choice == "3":
                print("\nNested blocks challenge:")
                n = int(input("Enter number of rows (1-8): ") or 5)
                for i in range(1, n+1):
                    if i % 2 == 0:
                        print("    " * i + f"Even row {i}")
                    else:
                        print("  " * i + f"Odd row {i}")
                print("→ Notice how inner if block is indented further")

            elif choice == "4":
                print("\nCreate your own function (we'll check indentation):")
                print("Try writing a small function that prints even numbers up to N.")
                n = int(input("Enter N: ") or 10)
                print("Correct structure would be:")
                print("def print_even(n):")
                print("    for i in range(n+1):")
                print("        if i % 2 == 0:")
                print("            print(i)")
                print("\n(You can copy this pattern in real code)")

            elif choice == "5":
                print("\nCommon Indentation Mistakes Quiz:")
                print("1. Mixing tabs and spaces → IndentationError")
                print("2. Forgetting to indent after ':' → IndentationError")
                print("3. Unindenting too early or too late → unexpected indent")
                print("4. Using 2 spaces in one place and 4 in another → Error")
                print("→ Always use 4 spaces consistently!")

            else:
                print("Please choose 1-5.")

        except ValueError:
            print("✗ Please enter a valid number.")
        except Exception as e:
            print(f"✗ Something went wrong: {e}")

    print("\nWell done! You now understand why Python cares so much about indentation.")
    print("Consistent 4-space indentation is a core part of writing clean Python.")
    print("Next: While Loops (Day 15).\n")


if __name__ == "__main__":
    main()