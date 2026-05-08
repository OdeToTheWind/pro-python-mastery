# tests/test_day_42.py
import os

def test_directory_operations():
    test_dir = "test_dir_42"
    os.makedirs(test_dir, exist_ok=True)
    assert os.path.exists(test_dir)
    os.rmdir(test_dir)
    assert not os.path.exists(test_dir)