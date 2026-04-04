# src/day_24_debugging_techniques/main.py
"""
Day 24: Debugging Techniques – Interactive Explorer
Learn practical debugging strategies: print debugging, reading tracebacks, 
using breakpoint(), and common bug patterns.
"""

def print_debugging_guide():
    print("\n" + "═" * 70)
    print("Debugging Techniques – Quick Reference (Day 24)")
    print("═" * 70)
    print("1. Print Debugging     → Add strategic print() statements")
    print("2. Read Tracebacks     → Understand error messages")
    print("3. breakpoint() / pdb  → Interactive debugger")
    print("4. Rubber Duck Debugging → Explain code to an object")
    print("5. Common Bugs         → Off-by-one, NoneType, IndexError, etc.")
    print("")
    print("Best Practice:")
    print("• Start with the traceback")
    print("• Reproduce the bug reliably")
    print("• Isolate the problem")
    print("• Fix and test")
    print("═" * 70)


def main():
    print("Welcome to Day 24 – Debugging Techniques!")
    print("The final day of Beginner Projects. Let's learn how to find and fix bugs.\n")

    print_debugging_guide()

    while True:
        print("\n" + "─" * 60)
        print("Choose a Debugging Scenario:")
        print("  1) Reading and Understanding Tracebacks")
        print("  2) Print Debugging Strategy")
        print("  3) Common Bug: IndexError & Off-by-One")
        print("  4) Common Bug: NoneType / TypeError")
        print("  5) Common Bug: Logic Error (Silent Bug)")
        print("  6) Interactive Bug Hunt Game")
        print("  7) Using breakpoint() Simulation")
        print("─" * 60)

        choice = input("→ ").strip().lower()

        if choice in ('quit', 'q', 'exit'):
            break

        try:
            if choice == "1":
                print("\n🔍 Reading Tracebacks")
                print("Example error you might see:")
                print("Traceback (most recent call last):")
                print("  File 'main.py', line 42, in <module>")
                print("    print(my_list[10])")
                print("IndexError: list index out of range")
                print("\nKey parts:")
                print("• Last line = where the error happened")
                print("• File and line number = where to look")
                print("• Error type (IndexError, ValueError, etc.)")

            elif choice == "2":
                print("\n🖨️  Print Debugging Strategy")
                numbers = [5, 12, 8, 3, 19]
                print("Finding the maximum with print debugging:")
                max_val = numbers[0]
                for i, num in enumerate(numbers):
                    print(f"Step {i}: Current number = {num}, Current max = {max_val}")
                    if num > max_val:
                        max_val = num
                        print(f"  → New max found: {max_val}")
                print(f"Final maximum: {max_val}")

            elif choice == "3":
                print("\n🐛 Common Bug: IndexError / Off-by-One")
                lst = ["apple", "banana", "cherry"]
                print(f"List: {lst} (length = {len(lst)})")
                
                try:
                    index = int(input("Enter index to access (0-2): "))
                    print(f"Item at index {index}: {lst[index]}")
                except IndexError:
                    print("IndexError! Remember: indices go from 0 to len-1")
                    print("Common fix: Check index < len(list)")

            elif choice == "4":
                print("\n🐛 Common Bug: NoneType / TypeError")
                def get_user():
                    # Simulate sometimes returning None
                    return None
                
                user = get_user()
                print("Trying to use the result...")
                try:
                    print(f"User name length: {len(user)}")
                except TypeError:
                    print("TypeError: 'NoneType' object has no len()")
                    print("Common fix: Add None check -> if user is not None:")

            elif choice == "5":
                print("\n🐛 Silent Logic Bug")
                print("Bug: Calculate average but forget to handle empty list")
                scores = []
                # Buggy code:
                # avg = sum(scores) / len(scores)
                
                # Fixed version:
                if scores:
                    avg = sum(scores) / len(scores)
                    print(f"Average: {avg}")
                else:
                    print("Cannot calculate average of empty list")

            elif choice == "6":
                print("\n🔎 Interactive Bug Hunt Game")
                print("Find the bug in this small program:")
                print("def calculate_total(items):")
                print("    total = 0")
                print("    for item in items:")
                print("        total = total + item  # Bug is here?")
                print("    return total")
                
                guess = input("\nWhat is the bug? (or 'run' to test): ").strip().lower()
                if guess == "run":
                    print("Running with [10, 20, 30] → Result should be 60")
                    # Corrected version for demo
                    def calculate_total(items):
                        return sum(items)
                    print("Correct result:", calculate_total([10, 20, 30]))

            elif choice == "7":
                print("\n🔧 breakpoint() Simulation")
                print("In real code you can insert `breakpoint()` to pause execution")
                print("Here we simulate it:")
                x = 10
                y = 20
                print(f"Before breakpoint: x={x}, y={y}")
                # breakpoint() would pause here in real Python 3.7+
                print("Imagine debugger is active now...")
                z = x + y
                print(f"After calculation: z={z}")

            else:
                print("Please choose 1-7.")

        except ValueError:
            print("✗ Please enter valid numbers.")
        except Exception as e:
            print(f"✗ Error: {e}")

    print("\n🎉 Congratulations! You have completed all 24 Beginner Projects.")
    print("You now have a strong foundation in Python programming.")
    print("Next stage: Intermediate Projects starting from Day 25.")
    print("Well done on this journey!\n")


if __name__ == "__main__":
    main()