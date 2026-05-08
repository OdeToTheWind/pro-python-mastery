# tests/test_day_45.py
def test_list_comprehensions():
    numbers = list(range(1, 11))
    squares = [x**2 for x in numbers]
    evens = [x for x in numbers if x % 2 == 0]
    
    assert squares[:5] == [1, 4, 9, 16, 25]
    assert evens == [2, 4, 6, 8, 10]