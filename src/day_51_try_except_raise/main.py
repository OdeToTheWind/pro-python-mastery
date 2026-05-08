# src/day_51_try_except_raise/main.py
"""
Day 51: Try / Except / Raise – Interactive Error Handling Explorer
"""

def main():
    print("Welcome to Day 51 – Try / Except / Raise\n")

    while True:
        print("\n" + "─" * 60)
        print("Choose Error Scenario:")
        print("  1) Division by Zero")
        print("  2) Invalid Input (ValueError)")
        print("  3) File Not Found")
        print("  4) Custom Exception")
        print("  5) Exit")
        print("─" * 60)

        choice = input("→ ").strip()

        if choice == "5":
            break

        try:
            if choice == "1":
                a = int(input("Numerator: "))
                b = int(input("Denominator: "))
                result = a / b
                print(f"Result: {result}")

            elif choice == "2":
                text = input("Enter a number: ")
                num = int(text)
                print(f"Converted: {num}")

            elif choice == "3":
                filename = input("Enter filename: ")
                with open(filename, "r") as f:
                    print(f.read())

            elif choice == "4":
                age = int(input("Enter your age: "))
                if age < 0:
                    raise ValueError("Age cannot be negative!")
                print(f"Age {age} is valid.")

        except ZeroDivisionError:
            print("❌ Cannot divide by zero!")
        except ValueError as e:
            print(f"❌ ValueError: {e}")
        except FileNotFoundError:
            print("❌ File not found!")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        else:
            print("✅ No error occurred!")
        finally:
            print("→ Finally block executed (cleanup)")

    print("\nYou now understand advanced error handling.")
    print("Next: Working with JSONs (Day 52)\n")


if __name__ == "__main__":
    main()