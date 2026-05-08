# tests/test_day_46.py
def test_dict_comprehension():
    squares = {x: x**2 for x in range(1, 6)}
    assert squares == {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}