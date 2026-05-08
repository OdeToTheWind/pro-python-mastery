# src/day_46_dictionary_comprehensions/main.py
"""
Day 46: Dictionary Comprehensions – Interactive Explorer
"""

def main():
    print("Welcome to Day 46 – Dictionary Comprehensions\n")

    while True:
        print("\n" + "─" * 50)
        print("Dictionary Comprehension Examples:")
        print("  1) Square numbers as dict")
        print("  2) Filter even numbers")
        print("  3) Word length mapping")
        print("  4) Custom comprehension")
        print("  5) Exit")
        print("─" * 50)

        choice = input("→ ").strip()

        if choice == "5":
            break

        if choice == "1":
            squares = {x: x**2 for x in range(1, 11)}
            print("Squares:", squares)

        elif choice == "2":
            evens = {x: x**2 for x in range(1, 21) if x % 2 == 0}
            print("Even squares:", evens)

        elif choice == "3":
            words = ["python", "programming", "comprehension", "dictionary"]
            word_length = {word: len(word) for word in words}
            print("Word lengths:", word_length)

        elif choice == "4":
            numbers = range(1, 11)
            custom = {x: "even" if x % 2 == 0 else "odd" for x in numbers}
            print("Number classification:", custom)

    print("\nDictionary comprehensions are powerful for creating mappings.")
    print("Next: Packing and Unpacking (Day 47)\n")


if __name__ == "__main__":
    main()