# tests/test_day_52.py
import json

def test_json_serialization():
    data = {"name": "Test", "score": 95}
    json_str = json.dumps(data)
    loaded = json.loads(json_str)
    assert loaded["name"] == "Test"