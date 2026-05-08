# tests/test_day_55.py
from datetime import datetime, timedelta

def test_date_operations():
    now = datetime.now()
    future = now + timedelta(days=10)
    assert future > now