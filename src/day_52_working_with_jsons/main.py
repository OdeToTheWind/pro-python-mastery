# src/day_52_working_with_jsons/main.py
"""
Day 52: Working with JSONs – Interactive Explorer
"""

import json

def main():
    print("Welcome to Day 52 – Working with JSONs\n")

    data = {
        "students": [
            {"name": "Aarav", "age": 16, "marks": 92},
            {"name": "Diya", "age": 15, "marks": 88}
        ]
    }

    filename = "students.json"

    while True:
        print("\n" + "─" * 50)
        print("JSON Operations:")
        print("  1) Save data to JSON")
        print("  2) Load data from JSON")
        print("  3) Exit")
        print("─" * 50)

        choice = input("→ ").strip()

        if choice == "3":
            break

        if choice == "1":
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print(f"✅ Data saved to {filename}")

        elif choice == "2":
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                print("Loaded Data:")
                print(json.dumps(loaded, indent=2))
            except FileNotFoundError:
                print("File not found. Save data first.")

    print("\nJSON handling completed.")
    print("Next: Local Persistence (Day 53)\n")


if __name__ == "__main__":
    main()