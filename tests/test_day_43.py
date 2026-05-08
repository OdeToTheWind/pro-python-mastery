# tests/test_day_43.py
import csv
import os

def test_csv_write_read():
    test_file = "test_students.csv"
    data = [["Name", "Age"], ["Alice", "25"]]

    with open(test_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)

    with open(test_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows[0] == ["Name", "Age"]
    os.remove(test_file)