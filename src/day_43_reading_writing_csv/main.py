# src/day_43_reading_writing_csv/main.py
"""
Day 43: Reading and Writing to CSV – Interactive Explorer
"""

import os
import csv

def main():
    print("Welcome to Day 43 – CSV File Operations\n")
    filename = "students.csv"

    while True:
        print("\n" + "─" * 50)
        print("CSV Operations:")
        print("  1) Write new student data")
        print("  2) Read CSV file")
        print("  3) Exit")
        print("─" * 50)

        choice = input("→ ").strip()

        if choice == "3":
            break

        if choice == "1":
            name = input("Student Name: ").strip()
            age = input("Age: ").strip()
            grade = input("Grade: ").strip()
            marks = input("Total Marks: ").strip()

            with open(filename, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if os.stat(filename).st_size == 0:  # write header if file is empty
                    writer.writerow(["Name", "Age", "Grade", "Marks"])
                writer.writerow([name, age, grade, marks])
            print(f"✅ Data saved to {filename}")

        elif choice == "2":
            if os.path.exists(filename):
                with open(filename, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        print(row)
            else:
                print("No CSV file found yet.")

    print("\nCSV operations completed.")
    print("Next: Introduction to Pandas (Day 44)\n")


if __name__ == "__main__":
    main()