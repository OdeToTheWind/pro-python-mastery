# src/day_31_python_methods/main.py
"""
Day 31: Python Methods – Interactive Explorer
Instance methods, class methods, and static methods.
"""

class BankAccount:
    interest_rate = 0.05  # class attribute

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    # Instance method
    def deposit(self, amount):
        self.balance += amount
        return f"Deposited ₹{amount}. New balance: ₹{self.balance}"

    # Instance method
    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds!"
        self.balance -= amount
        return f"Withdrew ₹{amount}. New balance: ₹{self.balance}"

    # Class method
    @classmethod
    def set_interest_rate(cls, rate):
        cls.interest_rate = rate
        return f"Interest rate updated to {rate*100}%"

    # Static method
    @staticmethod
    def is_valid_amount(amount):
        return amount > 0


def main():
    print("Welcome to Day 31 – Python Methods\n")

    account = BankAccount("Alice", 1000)

    while True:
        print("\n" + "─" * 50)
        print("Choose action:")
        print("  1) Deposit")
        print("  2) Withdraw")
        print("  3) Show Balance")
        print("  4) Update Interest Rate (Class Method)")
        print("  5) Check Valid Amount (Static Method)")
        print("  6) Exit")
        print("─" * 50)

        choice = input("→ ").strip()

        if choice == "6":
            break

        if choice == "1":
            amt = float(input("Enter deposit amount: "))
            if BankAccount.is_valid_amount(amt):
                print(account.deposit(amt))
            else:
                print("Invalid amount!")

        elif choice == "2":
            amt = float(input("Enter withdraw amount: "))
            print(account.withdraw(amt))

        elif choice == "3":
            print(f"Current balance: ₹{account.balance}")

        elif choice == "4":
            rate = float(input("Enter new interest rate (e.g. 0.06 for 6%): "))
            print(BankAccount.set_interest_rate(rate))

        elif choice == "5":
            amt = float(input("Enter amount to validate: "))
            print("Valid amount" if BankAccount.is_valid_amount(amt) else "Invalid amount")

    print("\nYou now understand instance, class, and static methods!")
    print("Next: Class Initialisers (Day 32)\n")


if __name__ == "__main__":
    main()