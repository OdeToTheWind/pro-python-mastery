# tests/test_day_40.py
def test_slicing():
    s = "PythonProgramming"
    assert s[:6] == "Python"
    assert s[-6:] == "amming"
    assert s[::2] == "PtoPormig"
    assert s[::-1] == "gnimmargorPnohtyP"