# src/day_16_flowchart_programming/main.py
"""
Day 16: Flowchart Programming – Interactive Translator
Learn how to read, understand, and convert flowcharts into Python code.
"""

def print_flowchart_guide():
    print("\n" + "═" * 70)
    print("Flowchart Programming – Quick Reference (Day 16)")
    print("═" * 70)
    print("Common Flowchart Symbols:")
    print("• Oval       → Start / End")
    print("• Rectangle  → Process / Action")
    print("• Diamond    → Decision (Yes/No)")
    print("• Parallelogram → Input / Output")
    print("• Arrow      → Flow direction")
    print("")
    print("Translation Rules:")
    print("• Diamond (Decision) → if / elif / else")
    print("• Rectangle          → normal statements")
    print("• Loop arrows        → while or for loops")
    print("• Multiple paths     → nested if or elif chains")
    print("═" * 70)


def main():
    print("Welcome to Day 16 – Flowchart Programming!")
    print("We'll convert real flowcharts into working Python code interactively.\n")

    print_flowchart_guide()

    while True:
        print("\n" + "─" * 60)
        print("Choose a Flowchart to Convert into Code:")
        print("  1) Simple Eligibility Checker")
        print("  2) Grade Calculator Flowchart")
        print("  3) Number Guessing Game Flowchart")
        print("  4) Discount Calculator")
        print("  5) Login System with Retry Limit")
        print("  6) Custom Flowchart Builder (Simple)")
        print("─" * 60)

        choice = input("→ ").strip()

        if choice.lower() in ('quit', 'q', 'exit'):
            break

        try:
            if choice == "1":
                print("\nFlowchart: Eligibility Checker")
                print("Start → Input Age → Age >= 18? → Yes → Input License → Has License? → Yes → Eligible")
                print("                                           → No  → Not Eligible")
                print("                                           → No  → Not Eligible\n")

                age = int(input("Enter your age: "))
                if age >= 18:
                    has_license = input("Do you have a driving license? (y/n): ").strip().lower()
                    if has_license == 'y':
                        print("✅ You are eligible to drive!")
                    else:
                        print("❌ You need a driving license.")
                else:
                    print("❌ You must be 18 or older.")

            elif choice == "2":
                print("\nFlowchart: Grade Calculator")
                print("Input Score → Score >= 90? → A+")
                print("            → Score >= 80? → A")
                print("            → Score >= 70? → B  ... and so on\n")

                score = float(input("Enter your score (0-100): "))
                if score >= 90:
                    grade = "A+"
                elif score >= 80:
                    grade = "A"
                elif score >= 70:
                    grade = "B"
                elif score >= 60:
                    grade = "C"
                elif score >= 50:
                    grade = "D"
                else:
                    grade = "F"
                print(f"Your grade is: {grade}")

            elif choice == "3":
                print("\nFlowchart: Number Guessing Game")
                print("This flowchart has a loop with decision diamonds.\n")
                import random
                secret = random.randint(1, 50)
                attempts = 0
                max_attempts = 8

                print("Guess the secret number (1-50). You have 8 attempts.\n")

                while attempts < max_attempts:
                    guess = int(input(f"Attempt {attempts+1}/{max_attempts}: "))
                    attempts += 1

                    if guess == secret:
                        print(f"🎉 Correct! You guessed it in {attempts} attempts!")
                        break
                    elif guess < secret:
                        print("Too low ↑")
                    else:
                        print("Too high ↓")
                else:
                    print(f"Game Over! The number was {secret}.")

            elif choice == "4":
                print("\nFlowchart: Discount Calculator")
                amount = float(input("Enter purchase amount (₹): "))
                
                if amount > 10000:
                    discount = 0.20
                    print("20% discount applied (Premium customer)")
                elif amount > 5000:
                    discount = 0.10
                    print("10% discount applied")
                elif amount > 2000:
                    discount = 0.05
                    print("5% discount applied")
                else:
                    discount = 0.0
                    print("No discount")

                final_price = amount * (1 - discount)
                print(f"Final price after discount: ₹{final_price:.2f}")

            elif choice == "5":
                print("\nFlowchart: Login System with 3 attempts")
                correct_pin = "1234"
                attempts = 0

                while attempts < 3:
                    pin = input("Enter 4-digit PIN: ")
                    attempts += 1
                    if pin == correct_pin:
                        print("✅ Login Successful! Welcome.")
                        break
                    else:
                        print(f"❌ Wrong PIN. {3 - attempts} attempts remaining.")
                else:
                    print("❌ Too many failed attempts. Account temporarily locked.")

            elif choice == "6":
                print("\nCustom Simple Flowchart Builder")
                print("We'll build a basic decision flowchart together.")
                age = int(input("Enter age: "))
                if age >= 18:
                    print("Adult branch:")
                    student = input("Are you a student? (y/n): ").lower()
                    if student == 'y':
                        print("→ Student discount available")
                    else:
                        print("→ Regular adult pricing")
                else:
                    print("→ Minor branch: Parent consent required")

            else:
                print("Please choose 1-6.")

        except ValueError:
            print("✗ Please enter valid numbers.")
        except Exception as e:
            print(f"✗ Error: {e}")

    print("\nGreat work translating flowcharts into Python code!")
    print("You now understand how to convert visual logic into working programs.")
    print("Next: Positional and Keyword Arguments (Day 17).\n")


if __name__ == "__main__":
    main()