# src/day_50_error_handling_exceptions/main.py
"""
Day 50: Error Handling and Exceptions – Interactive Explorer
"""

def main():
    print("Welcome to Day 50 – Error Handling and Exceptions\n")

    while True:
        print("\n" + "─" * 50)
        print("Choose error scenario:")
        print("  1) Division by Zero")
        print("  2) ValueError (int conversion)")
        print("  3) File Not Found")
        print("  4) Exit")
        print("─" * 50)

        choice = input("→ ").strip()

        if choice == "4":
            break

        try:
            if choice == "1":
                a = int(input("Enter numerator: "))
                b = int(input("Enter denominator: "))
                result = a / b
                print(f"Result: {result}")

            elif choice == "2":
                text = input("Enter text to convert to int: ")
                num = int(text)
                print(f"Converted: {num}")

            elif choice == "3":
                filename = input("Enter filename to read: ")
                with open(filename, "r") as f:
                    print(f.read())

        except ZeroDivisionError:
            print("❌ Error: Division by zero is not allowed!")
        except ValueError:
            print("❌ Error: Invalid input! Expected a number.")
        except FileNotFoundError:
            print("❌ Error: File not found!")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    print("\nYou now understand robust error handling.")
    print("End of selected Intermediate days.")


if __name__ == "__main__":
    main()