# src/day_28_classes/main.py
"""
Day 28: Creating Classes in Python – Interactive Explorer
"""

class Student:
    """Simple Student class example"""
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def introduce(self):
        return f"Hi, I'm {self.name}, {self.age} years old, in grade {self.grade}."

    def is_adult(self):
        return self.age >= 18


def main():
    print("Welcome to Day 28 – Creating Classes in Python\n")

    students = []
    while True:
        name = input("Enter student name (or 'done' to finish): ").strip()
        if name.lower() == 'done':
            break
        try:
            age = int(input("Enter age: "))
            grade = input("Enter grade: ").strip()
            student = Student(name, age, grade)
            students.append(student)
            print(f"Created student: {student.introduce()}\n")
        except ValueError:
            print("Invalid age. Try again.\n")

    print("\nAll Students:")
    for s in students:
        status = "Adult" if s.is_adult() else "Minor"
        print(f"• {s.name} ({status}) - Grade {s.grade}")

    print("\nYou have successfully created and used your first Python classes!")
    print("Next: Using External Python Modules (Day 29)\n")


if __name__ == "__main__":
    main()