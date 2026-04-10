# src/day_30_getting_setting_attributes/main.py
"""
Day 30: Getting / Setting Attributes – Interactive Explorer
Using @property, getters, and setters with proper input handling.
"""

class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value

    def introduce(self):
        return f"My name is {self.name} and I am {self.age} years old."


def main():
    print("Welcome to Day 30 – Getting / Setting Attributes\n")

    p = Person("Alice", 25)
    print(p.introduce())

    while True:
        age_input = input("Change age to (or type 'skip' to continue): ").strip()
        if age_input.lower() == 'skip':
            break
        try:
            new_age = int(age_input)
            p.age = new_age
            print(f"Updated: {p.introduce()}")
            break
        except ValueError:
            print("❌ Please enter a valid integer for age.")
        except Exception as e:
            print(f"❌ Error: {e}")

    print("\nYou now understand @property and setters!")
    print("Next topic coming soon.\n")


if __name__ == "__main__":
    main()