# src/day_13_for_loops/main.py
"""
Day 13: For Loops in Python – Interactive Explorer
Master for loops, range(), enumerate(), zip(), nested loops, and real-world use cases.
"""

def print_for_loop_cheat_sheet():
    print("\n" + "═" * 70)
    print("For Loops in Python – Quick Reference (Day 13)")
    print("═" * 70)
    print("for item in sequence:          → Iterate over list, tuple, string, dict, etc.")
    print("for i in range(start, stop, step): → Generate sequence of numbers")
    print("enumerate(seq)                 → Get (index, value) pairs")
    print("zip(list1, list2)              → Iterate multiple sequences together")
    print("for ... else:                  → else runs if no break occurred")
    print("Nested loops                   → Loop inside another loop")
    print("═" * 70)


def main():
    print("Welcome to Day 13 – For Loops in Python!")
    print("Let's explore iteration with interactive examples and mini-projects.\n")

    print_for_loop_cheat_sheet()

    while True:
        print("\n" + "─" * 60)
        print("Choose a For Loop Demo (or 'quit' to exit):")
        print("  1) Basic iteration over list & string")
        print("  2) Number patterns with range()")
        print("  3) Multiplication Table Generator")
        print("  4) Enumerate – Show index + value")
        print("  5) Zip – Combine multiple lists")
        print("  6) Shopping Cart Total Calculator")
        print("  7) Nested Loop – Simple Star Pyramid")
        print("─" * 60)

        choice = input("→ ").strip().lower()

        if choice in ('quit', 'q', 'exit'):
            break

        try:
            if choice == "1":
                items = input("Enter comma-separated items: ").strip()
                if not items:
                    items = "apple,banana,cherry,mango"
                item_list = [x.strip() for x in items.split(',')]
                
                print("\nIterating with for loop:")
                for item in item_list:
                    print(f"  • {item}")
                
                print("\nIterating over string characters:")
                word = input("Enter a word: ").strip() or "Python"
                for char in word:
                    print(f"  → {char}")

            elif choice == "2":
                start = int(input("Start number: ") or 1)
                end = int(input("End number (exclusive): ") or 11)
                step = int(input("Step (default 1): ") or 1)
                
                print(f"\nNumbers from {start} to {end-1} with step {step}:")
                for i in range(start, end, step):
                    print(i, end=" ")
                print()

            elif choice == "3":
                n = int(input("Enter number for multiplication table: "))
                print(f"\nMultiplication Table of {n}:")
                for i in range(1, 11):
                    print(f"{n} × {i:2d} = {n * i:3d}")

            elif choice == "4":
                fruits = ["apple", "banana", "cherry", "date", "elderberry"]
                print("\nUsing enumerate():")
                for index, fruit in enumerate(fruits, start=1):
                    print(f"{index:2d}. {fruit}")

            elif choice == "5":
                names = ["Alice", "Bob", "Charlie"]
                scores = [85, 92, 78]
                print("\nUsing zip() to combine names and scores:")
                for name, score in zip(names, scores):
                    print(f"{name:8} → {score} marks")

            elif choice == "6":
                print("Enter items with price (format: item=price), one per line.")
                print("Type 'done' when finished.")
                total = 0
                items = []
                while True:
                    line = input()
                    if line.lower() == 'done':
                        break
                    if '=' in line:
                        item, price_str = line.split('=', 1)
                        try:
                            price = float(price_str.strip())
                            items.append((item.strip(), price))
                            total += price
                        except ValueError:
                            print("Invalid price format.")
                
                print("\nYour Shopping Cart:")
                for item, price in items:
                    print(f"  • {item:15} ₹{price:6.2f}")
                print(f"{'─' * 30}")
                print(f"Total Amount: ₹{total:.2f}")

            elif choice == "7":
                rows = int(input("Enter number of rows for pyramid (max 15): ") or 5)
                rows = min(rows, 15)
                print("\nStar Pyramid:")
                for i in range(1, rows + 1):
                    print(" " * (rows - i) + "* " * i)

            else:
                print("Invalid choice. Please select 1-7.")

        except ValueError:
            print("✗ Please enter valid numbers.")
        except Exception as e:
            print(f"✗ Error: {e}")

    print("\nFantastic! You now master For Loops.")
    print("Next up: While Loops (Day 15) after Code Blocks & Indentation (Day 14).\n")


if __name__ == "__main__":
    main()