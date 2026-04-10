# src/day_27_oop_basics/main.py
"""
Day 27: Python Object Oriented Programming – Interactive Explorer
"""

class Student:
    def __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade

    def introduce(self):
        return f"Hi, I'm {self.name}, a {self.age} year old student in grade {self.grade}."

    def is_adult(self):
        return self.age >= 18


class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.speed = 0

    def accelerate(self, increase):
        self.speed += increase
        return f"Speed is now {self.speed} km/h"


def main():
    print("Welcome to Day 27 – Python Object Oriented Programming\n")

    # Create students
    s1 = Student("Aarav", 16, "10th")
    s2 = Student("Diya", 15, "9th")

    print(s1.introduce())
    print(s2.introduce())
    print(f"Is {s1.name} an adult? {s1.is_adult()}\n")

    # Create car
    my_car = Car("Toyota", "Corolla", 2022)
    print(f"Created car: {my_car.make} {my_car.model} ({my_car.year})")
    print(my_car.accelerate(30))
    print(my_car.accelerate(20))

    print("\nYou have now created and used your own classes and objects!")
    print("Next: Creating Classes in Python (Day 28)\n")


if __name__ == "__main__":
    main()