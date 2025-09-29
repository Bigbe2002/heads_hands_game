import pytest
from game import Player, Monster, ArgumentError

def test_player_heal_limits():
    p = Player("Hero", 10, 10, 100, (1, 6))
    p.health = 50
    restored = p.heal()
    assert restored > 0
    assert p.health > 50
    for _ in range(3):
        p.heal()
    with pytest.raises(ArgumentError):
        p.heal()

def test_attack_damage_and_death():
    p = Player("Hero", 30, 1, 10, (5, 5))
    m = Monster("Orc", 1, 1, 5, (1, 1))
    hit, dmg = p.attack_target(m)
    if hit:
        assert dmg == 5
        assert m.health <= 0 or m.health == 0
    else:
        assert dmg == 0

def test_invalid_arguments():
    with pytest.raises(ArgumentError):
        Player("", 5, 5, 100, (1, 6))
    with pytest.raises(ArgumentError):
        Monster("Goblin", 40, 5, 100, (1, 6))
    with pytest.raises(ArgumentError):
        Monster("Goblin", 10, 5, -10, (1, 6))
    with pytest.raises(ArgumentError):
        Monster("Goblin", 10, 5, 100, (0, 6))
