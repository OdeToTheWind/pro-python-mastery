# src/day_42_file_directories/main.py
"""
Day 42: File Directories – Interactive Explorer
"""

import os
from pathlib import Path

def main():
    print("Welcome to Day 42 – Working with File Directories\n")

    while True:
        print("\n" + "─" * 50)
        print("Directory Operations:")
        print("  1) List current directory contents")
        print("  2) Create new folder")
        print("  3) Delete folder")
        print("  4) Show current working directory")
        print("  5) Exit")
        print("─" * 50)

        choice = input("→ ").strip()

        if choice == "5":
            break

        if choice == "1":
            print("\nCurrent directory contents:")
            for item in os.listdir("."):
                item_type = "📁 Folder" if os.path.isdir(item) else "📄 File"
                print(f"  {item_type} : {item}")

        elif choice == "2":
            folder_name = input("Enter folder name to create: ").strip()
            if folder_name:
                os.makedirs(folder_name, exist_ok=True)
                print(f"✅ Folder '{folder_name}' created.")

        elif choice == "3":
            folder_name = input("Enter folder name to delete: ").strip()
            if os.path.exists(folder_name) and os.path.isdir(folder_name):
                confirm = input(f"Delete '{folder_name}'? (y/n): ").lower()
                if confirm == 'y':
                    os.rmdir(folder_name)
                    print(f"✅ Folder '{folder_name}' deleted.")
            else:
                print("Folder not found.")

        elif choice == "4":
            print(f"Current working directory: {os.getcwd()}")

    print("\nFile directory operations completed.")
    print("Next: Reading and Writing to CSV (Day 43)\n")


if __name__ == "__main__":
    main()