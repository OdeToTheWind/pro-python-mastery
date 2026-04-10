# tests/test_day_30.py
import pytest
from src.day_30_getting_setting_attributes.main import Person

def test_person_property():
    p = Person("Bob", 30)
    assert p.name == "Bob"
    assert p.age == 30

    p.age = 35
    assert p.age == 35

    with pytest.raises(ValueError):
        p.age = -5