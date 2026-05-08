# tests/test_day_41.py
import os

def test_file_write_read():
    test_file = "test_file_io.txt"
    content = "Hello from test!"

    with open(test_file, "w", encoding="utf-8") as f:
        f.write(content)

    with open(test_file, "r", encoding="utf-8") as f:
        read_content = f.read()

    assert read_content == content
    os.remove(test_file)  # cleanup