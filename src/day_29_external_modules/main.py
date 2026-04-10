# src/day_29_external_modules/main.py
"""
Day 29: Using External Python Modules / Import – Interactive Explorer
"""

import random
import datetime
import math

def main():
    print("Welcome to Day 29 – Using External Python Modules\n")

    print("1. random module:")
    print(f"   Random number: {random.randint(1, 100)}")

    print("\n2. datetime module:")
    now = datetime.datetime.now()
    print(f"   Current date & time: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n3. math module:")
    print(f"   Square root of 16 = {math.sqrt(16)}")
    print(f"   Pi ≈ {math.pi:.6f}")

    print("\nYou can install more modules with: pip install <package-name>")
    print("Example: pip install requests pandas numpy")
    print("\nNext: Getting / Setting Attributes (Day 30)\n")


if __name__ == "__main__":
    main()