# src/day_45_list_comprehensions/main.py
"""
Day 45: List Comprehensions – Interactive Explorer
"""

def main():
    print("Welcome to Day 45 – List Comprehensions\n")

    numbers = list(range(1, 21))

    while True:
        print("\n" + "─" * 50)
        print("List Comprehension Examples:")
        print("  1) Squares of numbers")
        print("  2) Even numbers only")
        print("  3) Numbers divisible by 3")
        print("  4) Custom filter")
        print("  5) Exit")
        print("─" * 50)

        choice = input("→ ").strip()

        if choice == "5":
            break

        if choice == "1":
            squares = [x**2 for x in numbers]
            print("Squares:", squares)

        elif choice == "2":
            evens = [x for x in numbers if x % 2 == 0]
            print("Even numbers:", evens)

        elif choice == "3":
            multiples = [x for x in numbers if x % 3 == 0]
            print("Multiples of 3:", multiples)

        elif choice == "4":
            threshold = int(input("Show numbers greater than: "))
            result = [x for x in numbers if x > threshold]
            print(f"Numbers > {threshold}:", result)

    print("\nList comprehensions are a powerful and Pythonic way to create lists.")
    print("Next topics coming soon.\n")


if __name__ == "__main__":
    main()