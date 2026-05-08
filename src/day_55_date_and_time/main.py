# src/day_55_date_and_time/main.py
"""
Day 55: Working with Date and Time
"""

from datetime import datetime, timedelta

def main():
    print("Welcome to Day 55 – Working with Date and Time\n")

    now = datetime.now()
    print(f"Current date & time: {now}")
    print(f"Formatted: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    future = now + timedelta(days=30)
    print(f"30 days from now: {future.strftime('%Y-%m-%d')}")

    birth = input("Enter birth date (YYYY-MM-DD): ")
    try:
        bdate = datetime.strptime(birth, "%Y-%m-%d")
        age = (now - bdate).days // 365
        print(f"You are approximately {age} years old.")
    except:
        print("Invalid date format.")

    print("\nNext: Hosting with PythonAnywhere (Day 56)\n")


if __name__ == "__main__":
    main()