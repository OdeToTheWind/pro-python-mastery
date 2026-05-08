# src/day_41_file_io/main.py
"""
Day 41: File I/O – Reading and Writing to Local Files
"""

import os

def main():
    print("Welcome to Day 41 – File I/O (Reading & Writing Files)\n")

    filename = "notes.txt"

    while True:
        print("\n" + "─" * 50)
        print("File Operations:")
        print("  1) Write to file")
        print("  2) Read file")
        print("  3) Append to file")
        print("  4) Show file info")
        print("  5) Exit")
        print("─" * 50)

        choice = input("→ ").strip()

        if choice == "5":
            break

        try:
            if choice == "1":
                content = input("Enter text to write (will overwrite): ")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ Written to {filename}")

            elif choice == "2":
                if os.path.exists(filename):
                    with open(filename, "r", encoding="utf-8") as f:
                        content = f.read()
                    print(f"\n--- Content of {filename} ---")
                    print(content)
                else:
                    print("File does not exist yet.")

            elif choice == "3":
                content = input("Enter text to append: ")
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(content + "\n")
                print(f"✅ Appended to {filename}")

            elif choice == "4":
                if os.path.exists(filename):
                    size = os.path.getsize(filename)
                    print(f"File: {filename}")
                    print(f"Size: {size} bytes")
                else:
                    print("File does not exist.")

        except Exception as e:
            print(f"❌ Error: {e}")

    print("\nFile I/O operations completed.")
    print("Next: File Directories (Day 42)\n")


if __name__ == "__main__":
    main()