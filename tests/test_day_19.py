# tests/test_day_19.py
import pytest

def calculate_class_average(class_data: list) -> float:
    """Calculate average marks from list of student dicts"""
    if not class_data:
        return 0.0
    total = 0
    count = 0
    for student in class_data:
        total += sum(student["marks"].values())
        count += len(student["marks"])
    return round(total / count, 2)


def get_department_info(departments: dict, dept_name: str) -> dict:
    """Safe access to nested dictionary"""
    return departments.get(dept_name, {})


def test_class_average():
    students = [
        {"marks": {"math": 90, "science": 85}},
        {"marks": {"math": 88, "science": 92}}
    ]
    assert calculate_class_average(students) == 88.75


def test_empty_class_average():
    assert calculate_class_average([]) == 0.0


def test_nested_dict_access():
    depts = {
        "Engineering": {"employees": 25, "budget": 5000000},
        "Marketing": {"employees": 12, "budget": 1200000}
    }
    eng = get_department_info(depts, "Engineering")
    assert eng["employees"] == 25
    assert get_department_info(depts, "HR") == {}


def test_list_of_dicts_access():
    data = [
        {"name": "Aarav", "scores": [92, 88]},
        {"name": "Diya", "scores": [85, 90]}
    ]
    assert data[0]["name"] == "Aarav"
    assert data[1]["scores"][1] == 90