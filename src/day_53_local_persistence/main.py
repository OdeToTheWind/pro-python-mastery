# src/day_53_local_persistence/main.py
"""
Day 53: Local Persistence – Interactive Explorer
"""

import json
import os

FILE = "app_data.json"

def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {"score": 0, "level": 1}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def main():
    print("Welcome to Day 53 – Local Persistence\n")

    data = load_data()
    print(f"Loaded progress - Score: {data['score']}, Level: {data['level']}")

    while True:
        print("\n1. Add Score")
        print("2. Level Up")
        print("3. Show Progress")
        print("4. Exit")
        choice = input("→ ").strip()

        if choice == "4":
            save_data(data)
            print("Progress saved!")
            break

        if choice == "1":
            points = int(input("Points earned: "))
            data["score"] += points
        elif choice == "2":
            data["level"] += 1
            print(f"Level up! Now level {data['level']}")
        elif choice == "3":
            print(f"Current Progress: Score={data['score']}, Level={data['level']}")

    print("\nLocal persistence completed.")
    print("Next: Sending Email (Day 54)\n")


if __name__ == "__main__":
    main()