# src/day_39_python_inheritance/main.py
"""
Day 39: Python Inheritance – Interactive Explorer
"""

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "Some sound..."

    def eat(self):
        return f"{self.name} is eating."


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

    def speak(self):
        return "Woof Woof!"

    def fetch(self):
        return f"{self.name} fetched the ball!"


class Cat(Animal):
    def speak(self):
        return "Meow!"

    def climb(self):
        return f"{self.name} climbed the tree!"


def main():
    print("Welcome to Day 39 – Python Inheritance\n")

    dog = Dog("Buddy", "Golden Retriever")
    cat = Cat("Whiskers")

    print(dog.speak())
    print(cat.speak())
    print(dog.fetch())
    print(cat.climb())

    print("\nInheritance allows code reuse and hierarchical relationships.")
    print("Next: Python Slice Function (Day 40)\n")


if __name__ == "__main__":
    main()