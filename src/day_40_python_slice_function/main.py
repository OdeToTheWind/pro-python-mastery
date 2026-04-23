# src/day_40_python_slice_function/main.py
"""
Day 40: Python Slice Function – Interactive Explorer
"""

def main():
    print("Welcome to Day 40 – Python Slice Function\n")

    text = "PythonProgrammingIsFun"
    numbers = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    print(f"Original text: {text}")
    print(f"Original list: {numbers}\n")

    while True:
        print("Slice Examples:")
        print("  1) First 6 characters")
        print("  2) Last 4 characters")
        print("  3) Every 2nd character")
        print("  4) Reverse the string")
        print("  5) Custom slice")
        print("  6) Exit")
        
        choice = input("→ ").strip()

        if choice == "6":
            break

        if choice == "1":
            print("First 6:", text[:6])
        elif choice == "2":
            print("Last 4:", text[-4:])
        elif choice == "3":
            print("Every 2nd:", text[::2])
        elif choice == "4":
            print("Reversed:", text[::-1])
        elif choice == "5":
            start = int(input("Start index: ") or 0)
            end = int(input("End index: ") or len(text))
            step = int(input("Step: ") or 1)
            print("Custom slice:", text[start:end:step])

    print("\nSlicing is a powerful feature for working with sequences.")
    print("Next topics coming soon.\n")


if __name__ == "__main__":
    main()