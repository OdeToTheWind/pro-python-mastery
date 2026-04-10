# tests/test_day_27.py
from src.day_27_oop_basics.main import Student, Car

def test_student_class():
    s = Student("Test", 17, "10th")
    assert s.name == "Test"
    assert s.age == 17
    assert s.grade == "10th"
    assert "Test" in s.introduce()
    assert s.is_adult() is False

def test_car_class():
    c = Car("Honda", "City", 2023)
    assert c.make == "Honda"
    assert c.speed == 0
    c.accelerate(50)
    assert c.speed == 50