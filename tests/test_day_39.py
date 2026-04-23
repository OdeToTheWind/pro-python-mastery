# tests/test_day_39.py
from src.day_39_python_inheritance.main import Dog, Cat

def test_inheritance():
    dog = Dog("Max", "Labrador")
    cat = Cat("Luna")
    
    assert dog.speak() == "Woof Woof!"
    assert cat.speak() == "Meow!"
    assert "fetched" in dog.fetch()