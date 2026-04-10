# tests/test_day_28.py
from src.day_28_classes.main import Student

def test_student_class():
    s = Student("Test", 17, "10th")
    assert s.name == "Test"
    assert s.age == 17
    assert s.is_adult() is False
    assert "Test" in s.introduce()