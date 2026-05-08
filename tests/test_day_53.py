# tests/test_day_53.py
import json
import os
from src.day_53_local_persistence.main import load_data, save_data

def test_persistence():
    test_data = {"score": 100, "level": 5}
    save_data(test_data)
    loaded = load_data()
    assert loaded["score"] == 100
    os.remove("app_data.json")