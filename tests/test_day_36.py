# tests/test_day_36.py
from src.day_36_python_instances_and_state.main import Player

def test_player_state_independence():
    p1 = Player("Hero")
    p2 = Player("Villain")
    
    p1.take_damage(30)
    p2.take_damage(50)
    
    assert p1.health == 70
    assert p2.health == 50  # Different state per instance


def test_inventory_separate():
    p1 = Player("Hero")
    p2 = Player("Villain")
    
    p1.add_item("Sword")
    p2.add_item("Staff")
    
    assert "Sword" in p1.inventory
    assert "Staff" in p2.inventory
    assert "Sword" not in p2.inventory