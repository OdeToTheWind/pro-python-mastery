# src/day_11_error_handling/main.py
"""
Day 11: Error Handling in Python – Interactive Explorer
Learn try/except, else, finally, common exceptions, and graceful error recovery.
"""

def safe_input(prompt: str, expected_type=str):
    """Helper to get input with basic validation"""
    while True:
        try:
            value = input(prompt).strip()
            if value.lower() in ('quit', 'q', 'exit'):
                return None
            return expected_type(value)
        except ValueError:
            print(f"❌ Invalid input! Expected {expected_type.__name__}. Try again.")


def demonstrate_error_handling():
    print("\n" + "═" * 70)
    print("Common Exceptions & How to Handle Them")
    print("═" * 70)
    print("Exception              | When it happens                              | Typical Fix")
    print("───────────────────────┼──────────────────────────────────────────────┼────────────────────────────")
    print("ValueError             | Wrong value for conversion (int('abc'))      | try/except around conversion")
    print("TypeError              | Wrong type for operation (len(42))           | Check type or convert first")
    print("ZeroDivisionError      | Division by zero                             | Guard with if or except")
    print("IndexError             | List index out of range                      | Check length or use .get()")
    print("KeyError               | Dict key doesn't exist                       | Use .get() or try/except")
    print("FileNotFoundError      | Opening non-existent file                    | Check path or use try/except")
    print("═" * 70)


def main():
    print("Welcome to Day 11 – Error Handling in Python")
    print("We'll deliberately cause errors and learn how to handle them gracefully.\n")

    demonstrate_error_handling()

    while True:
        print("\n" + "─" * 60)
        print("Choose what to try (or 'quit' to exit):")
        print("  1) Number conversion (ValueError)")
        print("  2) Division calculator (ZeroDivisionError)")
        print("  3) List index access (IndexError)")
        print("  4) Dictionary lookup (KeyError)")
        print("  5) Password strength checker (multiple errors)")
        print("  6) Safe file reader simulation")
        print("─" * 60)

        choice = input("→ ").strip()

        if choice.lower() in ('quit', 'q', 'exit'):
            break

        try:
            if choice == "1":
                text = input("Enter something to convert to integer: ")
                number = int(text)
                print(f"✓ Success! {text} as integer is {number}")

            elif choice == "2":
                a = safe_input("Enter first number: ", float)
                if a is None: continue
                b = safe_input("Enter second number: ", float)
                if b is None: continue

                result = a / b
                print(f"✓ {a} / {b} = {result}")

            elif choice == "3":
                items = input("Enter comma-separated items: ").strip()
                if not items:
                    items = "apple,banana,cherry"
                lst = [x.strip() for x in items.split(',')]
                idx = safe_input(f"Enter index (0 to {len(lst)-1}): ", int)
                if idx is None: continue
                print(f"✓ Item at index {idx}: {lst[idx]}")

            elif choice == "4":
                data = {"name": "Alice", "age": 25, "city": "Bengaluru"}
                key = input("Enter key to lookup (name/age/city): ").strip().lower()
                print(f"✓ {key} = {data[key]}")

            elif choice == "5":
                pwd = input("Enter a password to check strength: ").strip()
                if len(pwd) < 8:
                    raise ValueError("Password must be at least 8 characters long")
                if not any(c.isdigit() for c in pwd):
                    raise ValueError("Password must contain at least one number")
                if not any(c.isupper() for c in pwd):
                    raise ValueError("Password must contain at least one uppercase letter")
                print("✓ Strong password! Well done.")

            elif choice == "6":
                filename = input("Enter filename to 'read' (e.g. notes.txt): ").strip() or "secret.txt"
                # Simulate file reading
                if "secret" in filename.lower():
                    raise FileNotFoundError(f"File '{filename}' not found (access restricted)")
                print(f"✓ Successfully read file: {filename}")
                print("   Content: This is a simulated file content...")

            else:
                print("Invalid option. Please choose 1-6.")

        except ValueError as e:
            print(f"✗ ValueError: {e}")
            print("   → This happens when the value is correct type but wrong content.")
        except ZeroDivisionError:
            print("✗ ZeroDivisionError: You cannot divide by zero!")
            print("   → Always check divisor != 0 or use try/except")
        except IndexError:
            print("✗ IndexError: List index out of range!")
            print("   → Always check length before accessing by index")
        except KeyError as e:
            print(f"✗ KeyError: '{e}' does not exist in the dictionary")
            print("   → Use .get(key, default) or check with 'in' before access")
        except FileNotFoundError as e:
            print(f"✗ FileNotFoundError: {e}")
            print("   → Common when working with files or paths")
        except Exception as e:   # Catch-all (not recommended in production)
            print(f"✗ Unexpected error: {type(e).__name__} - {e}")
        else:
            print("✓ No exception occurred — else block executed!")
        finally:
            print("→ finally block always runs (cleanup would go here)\n")

    print("\nExcellent work! You now know how to handle errors gracefully.")
    print("Key takeaway: Fail loudly during development, fail gracefully in production.\n")


if __name__ == "__main__":
    main()