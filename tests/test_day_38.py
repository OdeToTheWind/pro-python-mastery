# tests/test_day_38.py
from src.day_38_game_development_with_python_and_oop.main import Player, Enemy

def test_player_and_enemy():
    p = Player("Hero")
    e = Enemy("Goblin", 50)
    
    p.attack(e)
    assert e.health == 25
    
    p.heal()
    assert p.health <= 100