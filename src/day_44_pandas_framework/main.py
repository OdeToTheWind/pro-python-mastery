# src/day_44_pandas_framework/main.py
"""
Day 44: Introduction to Pandas – Interactive Explorer
"""

import pandas as pd

def main():
    print("Welcome to Day 44 – Introduction to Pandas\n")

    data = {
        "Name": ["Aarav", "Diya", "Rohan", "Meera"],
        "Age": [16, 15, 17, 16],
        "Grade": ["10th", "9th", "11th", "10th"],
        "Marks": [92, 88, 95, 89]
    }

    df = pd.DataFrame(data)

    while True:
        print("\n" + "─" * 50)
        print("Pandas Operations:")
        print("  1) Show DataFrame")
        print("  2) Show Statistics")
        print("  3) Filter Students (Marks > 90)")
        print("  4) Sort by Marks")
        print("  5) Exit")
        print("─" * 50)

        choice = input("→ ").strip()

        if choice == "5":
            break

        if choice == "1":
            print(df)
        elif choice == "2":
            print(df.describe())
        elif choice == "3":
            high_scorers = df[df["Marks"] > 90]
            print(high_scorers)
        elif choice == "4":
            print(df.sort_values(by="Marks", ascending=False))

    print("\nPandas is a powerful tool for data analysis.")
    print("Next: List Comprehensions (Day 45)\n")


if __name__ == "__main__":
    main()