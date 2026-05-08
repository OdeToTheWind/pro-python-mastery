# tests/test_day_47.py
def test_packing_unpacking():
    def sum_all(*args):
        return sum(args)
    assert sum_all(1, 2, 3) == 6