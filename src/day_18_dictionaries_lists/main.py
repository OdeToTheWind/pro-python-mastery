# src/day_18_dictionaries_lists/main.py
"""
Day 18: Python Dictionaries and Lists – Interactive Explorer
Master lists (mutable sequences) and dictionaries (key-value mappings).
"""

def print_cheat_sheet():
    print("\n" + "═" * 70)
    print("Lists vs Dictionaries – Quick Reference (Day 18)")
    print("═" * 70)
    print("LISTS:")
    print("• Ordered, mutable, allows duplicates")
    print("• Methods: append(), pop(), remove(), sort(), reverse(), extend()")
    print("• Access by index: mylist[0], slicing mylist[1:4]")
    print("")
    print("DICTIONARIES:")
    print("• Unordered (insertion order preserved since 3.7), mutable, unique keys")
    print("• Methods: .get(), .keys(), .values(), .items(), .update(), .pop()")
    print("• Access by key: mydict['key'], safer with .get(key, default)")
    print("═" * 70)


def student_info(name: str, age: int, grade: str = "10th", city: str = "Unknown") -> str:
    """Demonstrates default + keyword arguments with a student record."""
    return f"Student: {name}, Age: {age}, Grade: {grade}, City: {city}"


def create_order(customer: str, **details) -> dict:
    """Demonstrates **kwargs for building flexible dictionaries."""
    order = {"customer": customer}
    order.update(details)
    return order


def main():
    print("Welcome to Day 18 – Lists and Dictionaries in Python!")
    print("Let's explore these two powerful data structures interactively.\n")

    print_cheat_sheet()

    # Sample data for demos
    students = [
        {"name": "Aarav", "age": 16, "grade": "10th", "marks": 92},
        {"name": "Diya", "age": 15, "grade": "9th", "marks": 88},
        {"name": "Rohan", "age": 17, "grade": "11th", "marks": 95}
    ]

    while True:
        print("\n" + "─" * 60)
        print("Choose an Activity:")
        print("  1) List Operations (Shopping Cart)")
        print("  2) Dictionary Operations (Student Record)")
        print("  3) Combined: Student Management System")
        print("  4) List Methods Explorer")
        print("  5) Dictionary Methods Explorer")
        print("  6) Real-world Example: Inventory System")
        print("─" * 60)

        choice = input("→ ").strip().lower()

        if choice in ('quit', 'q', 'exit'):
            break

        try:
            if choice == "1":
                print("\n🛒 Shopping Cart using List")
                cart = []
                while True:
                    item = input("Add item (or 'done'): ").strip()
                    if item.lower() in ('done', 'quit'):
                        break
                    if item:
                        cart.append(item)
                        print(f"Added: {item} | Cart: {len(cart)} items")

                print("\nFinal Cart:", cart)
                if cart:
                    removed = cart.pop()
                    print(f"Removed last item: {removed}")

            elif choice == "2":
                print("\n📚 Student Record using Dictionary")
                student = {}
                student["name"] = input("Student Name: ").strip()
                student["age"] = int(input("Age: "))
                student["grade"] = input("Grade: ").strip()
                student["marks"] = int(input("Marks: "))

                print("\nStudent Record:")
                for key, value in student.items():
                    print(f"  {key.capitalize():8} : {value}")

                print(f"\nCity (safe get): {student.get('city', 'Not provided')}")

            elif choice == "3":
                print("\nStudent Management System (Lists + Dictionaries)")
                print("Current students:", [s["name"] for s in students])

                action = input("Add new student? (y/n): ").lower()
                if action == 'y':
                    new_student = {}
                    new_student["name"] = input("Name: ").strip()
                    new_student["age"] = int(input("Age: "))
                    new_student["grade"] = input("Grade: ").strip()
                    new_student["marks"] = int(input("Marks: "))
                    students.append(new_student)
                    print(f"Added {new_student['name']}!")

                print("\nAll Students:")
                for i, student in enumerate(students, 1):
                    print(f"{i}. {student['name']} - {student['grade']} - {student['marks']} marks")

            elif choice == "4":
                print("\nList Methods Explorer")
                fruits = ["apple", "banana", "cherry", "apple", "date"]
                print("Original:", fruits)
                fruits.append("elderberry")
                fruits.sort()
                print("After append + sort:", fruits)
                fruits.remove("apple")
                print("After removing one apple:", fruits)
                print("Count of 'apple':", fruits.count("apple"))

            elif choice == "5":
                print("\nDictionary Methods Explorer")
                person = {"name": "Meera", "age": 22}
                person.update({"city": "Bengaluru", "profession": "Engineer"})
                print("Updated dict:", person)
                print("Name:", person.get("name"))
                print("Salary (safe):", person.get("salary", "Not set"))
                removed = person.pop("age")
                print(f"Removed age: {removed}")
                print("Final dict:", person)

            elif choice == "6":
                print("\nInventory Management System")
                inventory = {"laptop": 15, "mouse": 50, "keyboard": 30}
                print("Current Inventory:", inventory)

                item = input("Item to update/add: ").strip().lower()
                qty = int(input(f"Quantity for {item}: "))
                inventory[item] = qty
                print(f"Updated/Added {item}: {qty}")
                print("Final Inventory:", inventory)

            else:
                print("Please choose 1-6.")

        except ValueError:
            print("✗ Please enter valid numbers.")
        except Exception as e:
            print(f"✗ Error: {e}")

    print("\nGreat work! You now understand Lists and Dictionaries deeply.")
    print("These two structures are used in almost every real Python project.\n")


if __name__ == "__main__":
    main()