# src/day_32_class_initialisers/main.py
"""
Day 32: Class Initialisers (__init__) – Interactive Explorer
"""

class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0, account_type: str = "Savings"):
        self.owner = owner
        self.balance = max(0.0, balance)  # prevent negative initial balance
        self.account_type = account_type
        print(f"✅ New {account_type} account created for {owner} with balance ₹{self.balance:.2f}")

    def deposit(self, amount: float):
        if amount > 0:
            self.balance += amount
            return f"Deposited ₹{amount:.2f}. New balance: ₹{self.balance:.2f}"
        return "Invalid deposit amount!"

    def withdraw(self, amount: float):
        if amount > self.balance:
            return "Insufficient funds!"
        if amount <= 0:
            return "Invalid withdrawal amount!"
        self.balance -= amount
        return f"Withdrew ₹{amount:.2f}. New balance: ₹{self.balance:.2f}"

    def show_info(self):
        return f"Owner: {self.owner} | Type: {self.account_type} | Balance: ₹{self.balance:.2f}"


def main():
    print("Welcome to Day 32 – Class Initialisers (__init__)\n")

    accounts = []

    while True:
        print("\n" + "─" * 50)
        print("1. Create New Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Show All Accounts")
        print("5. Exit")
        print("─" * 50)

        choice = input("→ ").strip()

        if choice == "5":
            break

        if choice == "1":
            name = input("Account Owner Name: ").strip()
            try:
                initial = float(input("Initial Balance (press Enter for 0): ") or 0)
                acc_type = input("Account Type (Savings/Current) [default: Savings]: ").strip() or "Savings"
                acc = BankAccount(name, initial, acc_type)
                accounts.append(acc)
            except ValueError:
                print("Invalid amount!")

        elif choice in ["2", "3"]:
            if not accounts:
                print("No accounts yet. Create one first.")
                continue
            print("Available accounts:")
            for i, acc in enumerate(accounts):
                print(f"{i+1}. {acc.show_info()}")
            idx = int(input("Select account number: ")) - 1
            if 0 <= idx < len(accounts):
                amt = float(input("Enter amount: "))
                if choice == "2":
                    print(accounts[idx].deposit(amt))
                else:
                    print(accounts[idx].withdraw(amt))
            else:
                print("Invalid account number.")

        elif choice == "4":
            if not accounts:
                print("No accounts created yet.")
            else:
                for acc in accounts:
                    print(acc.show_info())

    print("\nYou now understand how __init__ works as a constructor!")
    print("Next: Module Aliasing (Day 33)\n")


if __name__ == "__main__":
    main()