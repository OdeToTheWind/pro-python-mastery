# src/day_19_nested_collections/main.py
"""
Day 19: Nested Collections in Python – Interactive Explorer
Master lists of lists, lists of dictionaries, dictionaries of lists, and nested dicts.
"""

def print_nested_cheat_sheet():
    print("\n" + "═" * 70)
    print("Nested Collections – Quick Reference (Day 19)")
    print("═" * 70)
    print("Common Patterns:")
    print("• List of Dicts     → Database-like records (students, products)")
    print("• Dict of Lists     → Grouping data (class → student scores)")
    print("• List of Lists     → Grids, matrices, game boards")
    print("• Dict of Dicts     → Hierarchical data (user profiles with settings)")
    print("")
    print("Access Patterns:")
    print("• data[0]['key']          → list of dicts")
    print("• data['key'][0]          → dict of lists")
    print("• data[i][j]              → list of lists")
    print("• data['outer']['inner']  → nested dicts")
    print("═" * 70)


def main():
    print("Welcome to Day 19 – Nested Collections in Python!")
    print("We'll work with complex real-world data structures interactively.\n")

    print_nested_cheat_sheet()

    # Sample nested data
    classroom = {
        "10th A": [
            {"name": "Aarav", "marks": {"math": 92, "science": 88, "english": 95}},
            {"name": "Diya", "marks": {"math": 85, "science": 90, "english": 78}},
            {"name": "Rohan", "marks": {"math": 88, "science": 82, "english": 91}}
        ],
        "10th B": [
            {"name": "Meera", "marks": {"math": 95, "science": 89, "english": 87}},
            {"name": "Vikram", "marks": {"math": 76, "science": 80, "english": 82}}
        ]
    }

    while True:
        print("\n" + "─" * 60)
        print("Choose a Nested Collections Demo:")
        print("  1) List of Dictionaries (Student Database)")
        print("  2) Dictionary of Lists (Class-wise Scores)")
        print("  3) List of Lists (Simple Grid / Matrix)")
        print("  4) Dictionary of Dictionaries (User Profiles)")
        print("  5) Full Classroom Management System")
        print("  6) Nested Data Explorer")
        print("─" * 60)

        choice = input("→ ").strip().lower()

        if choice in ('quit', 'q', 'exit'):
            break

        try:
            if choice == "1":
                print("\nList of Dictionaries - Student Database")
                students = [
                    {"id": 101, "name": "Aarav", "age": 16, "subjects": ["Math", "Science"]},
                    {"id": 102, "name": "Diya", "age": 15, "subjects": ["English", "History"]}
                ]
                for student in students:
                    print(f"ID: {student['id']}, Name: {student['name']}, Age: {student['age']}")
                    print(f"  Subjects: {', '.join(student['subjects'])}")

            elif choice == "2":
                print("\nDictionary of Lists - Class-wise Scores")
                scores = {
                    "Math": [92, 85, 88, 95],
                    "Science": [88, 90, 82, 89],
                    "English": [95, 78, 91, 87]
                }
                for subject, marks_list in scores.items():
                    avg = sum(marks_list) / len(marks_list)
                    print(f"{subject:8} : {marks_list} → Average = {avg:.1f}")

            elif choice == "3":
                print("\nList of Lists - Simple Grid")
                grid = [
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                ]
                print("Matrix:")
                for row in grid:
                    print("  ", row)
                print(f"Center element: {grid[1][1]}")

            elif choice == "4":
                print("\nDictionary of Dictionaries - User Profiles")
                users = {
                    "user001": {"name": "Priya", "email": "priya@example.com", "settings": {"theme": "dark", "notifications": True}},
                    "user002": {"name": "Rahul", "email": "rahul@example.com", "settings": {"theme": "light", "notifications": False}}
                }
                username = input("Enter username to view (user001/user002): ").strip()
                if username in users:
                    user = users[username]
                    print(f"Name: {user['name']}")
                    print(f"Email: {user['email']}")
                    print(f"Theme: {user['settings']['theme']}")
                    print(f"Notifications: {user['settings']['notifications']}")
                else:
                    print("User not found.")

            elif choice == "5":
                print("\nFull Classroom Management System")
                print("Available classes:", list(classroom.keys()))
                selected_class = input("Select class (10th A / 10th B): ").strip()

                if selected_class in classroom:
                    print(f"\nStudents in {selected_class}:")
                    for student in classroom[selected_class]:
                        total = sum(student["marks"].values())
                        avg = total / len(student["marks"])
                        print(f"• {student['name']:10} | Marks: {student['marks']} | Avg: {avg:.1f}")

                    # Add new student
                    add = input("\nAdd a new student to this class? (y/n): ").lower()
                    if add == 'y':
                        new_name = input("Name: ").strip()
                        math = int(input("Math marks: "))
                        science = int(input("Science marks: "))
                        english = int(input("English marks: "))
                        classroom[selected_class].append({
                            "name": new_name,
                            "marks": {"math": math, "science": science, "english": english}
                        })
                        print(f"Added {new_name} successfully!")

            elif choice == "6":
                print("\nNested Data Explorer")
                data = {
                    "company": "TechCorp",
                    "departments": {
                        "Engineering": {"employees": 25, "budget": 5000000},
                        "Marketing": {"employees": 12, "budget": 1200000}
                    }
                }
                dept = input("Enter department (Engineering/Marketing): ").strip()
                if dept in data["departments"]:
                    info = data["departments"][dept]
                    print(f"{dept} Department:")
                    print(f"  Employees : {info['employees']}")
                    print(f"  Budget    : ₹{info['budget']:,}")
                else:
                    print("Department not found.")

            else:
                print("Please choose 1-6.")

        except ValueError:
            print("✗ Please enter valid numbers.")
        except KeyError as e:
            print(f"✗ Key not found: {e}")
        except Exception as e:
            print(f"✗ Error: {e}")

    print("\nExcellent! You now understand nested collections.")
    print("These structures are the foundation of most real-world Python applications.\n")


if __name__ == "__main__":
    main()