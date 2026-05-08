# src/day_49_strongly_dynamic_typing/main.py
"""
Day 49: Strongly Dynamic Typing in Python
"""

def main():
    print("Welcome to Day 49 – Strongly Dynamic Typing\n")

    # Dynamic typing examples
    var = 10
    print(f"var = {var} (type: {type(var).__name__})")

    var = "Hello Python"
    print(f"var = '{var}' (type: {type(var).__name__})")

    var = [1, 2, 3]
    print(f"var = {var} (type: {type(var).__name__})")

    print("\nPython is dynamically typed — types are determined at runtime.")
    print("This makes code flexible but requires careful testing.")


if __name__ == "__main__":
    main()