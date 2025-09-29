from __future__ import annotations
import random
from typing import Tuple

class ArgumentError(ValueError):
    pass

def _check_stat(name: str, value: int, min_v: int = 1, max_v: int = 30) -> None:
    if not isinstance(value, int):
        raise ArgumentError(f"{name} must be int, got {type(value).__name__}")
    if not (min_v <= value <= max_v):
        raise ArgumentError(f"{name} must be between {min_v} and {max_v}, got {value}")

def _check_damage_range(dmg: Tuple[int, int]) -> None:
    if (
        not isinstance(dmg, tuple)
        or len(dmg) != 2
        or not all(isinstance(x, int) for x in dmg)
    ):
        raise ArgumentError("damage_range must be a tuple of two ints (min, max)")
    a, b = dmg
    if a < 1 or b < a:
        raise ArgumentError("damage_range values must be natural numbers with min <= max")

class Creature:
    def __init__(
        self,
        name: str,
        attack: int,
        defense: int,
        max_health: int,
        damage_range: Tuple[int, int],
    ) -> None:
        if not isinstance(name, str) or not name:
            raise ArgumentError("name must be a non-empty string")
        _check_stat("attack", attack)
        _check_stat("defense", defense)
        if not isinstance(max_health, int) or max_health <= 0:
            raise ArgumentError("max_health must be a positive integer")
        _check_damage_range(damage_range)

        self.name = name
        self.attack = attack
        self.defense = defense
        self.max_health = max_health
        self.health = max_health
        self.damage_range = damage_range

    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, dmg: int) -> None:
        if not isinstance(dmg, int) or dmg < 0:
            raise ArgumentError("dmg must be a non-negative int")
        self.health = max(0, self.health - dmg)

    def _roll_d6(self) -> int:
        return random.randint(1, 6)

    def attack_target(self, other: "Creature") -> Tuple[bool, int]:
        if not isinstance(other, Creature):
            raise ArgumentError("other must be a Creature")
        if not self.is_alive():
            raise ArgumentError("dead creatures cannot attack")
        if not other.is_alive():
            raise ArgumentError("cannot attack a dead creature")

        modifier = self.attack - other.defense + 1
        dice_count = max(1, modifier)
        rolls = [self._roll_d6() for _ in range(dice_count)]
        success = any(r >= 5 for r in rolls)

        if success:
            dmg = random.randint(self.damage_range[0], self.damage_range[1])
            other.take_damage(dmg)
            return True, dmg
        else:
            return False, 0

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(name={self.name!r}, atk={self.attack}, def={self.defense}, "
            f"hp={self.health}/{self.max_health}, dmg={self.damage_range})"
        )

class Player(Creature):
    MAX_HEALS = 4
    HEAL_PERCENT = 0.3

    def __init__(self, name: str, attack: int, defense: int, max_health: int, damage_range: Tuple[int, int]) -> None:
        super().__init__(name, attack, defense, max_health, damage_range)
        self._heals_used = 0

    def heal(self) -> int:
        if not self.is_alive():
            raise ArgumentError("dead player cannot heal")
        if self._heals_used >= Player.MAX_HEALS:
            raise ArgumentError("no heals left")

        amount = int(self.max_health * Player.HEAL_PERCENT)
        if amount <= 0:
            amount = 1
        new_health = min(self.max_health, self.health + amount)
        restored = new_health - self.health
        self.health = new_health
        self._heals_used += 1
        return restored

    def heals_left(self) -> int:
        return max(0, Player.MAX_HEALS - self._heals_used)

class Monster(Creature):
    pass

if __name__ == "__main__":
    random.seed()
    player = Player("Hero", 10, 8, 100, (5, 12))
    goblin = Monster("Goblin", 7, 5, 40, (3, 6))

    print("--- Бой начинается ---")
    round_no = 1
    while player.is_alive() and goblin.is_alive():
        print(f"Раунд {round_no}")
        hit, dmg = player.attack_target(goblin)
        print("Игрок атакует:", "попал" if hit else "промах", f"урон {dmg}" if dmg else "")
        if not goblin.is_alive():
            print("Гоблин пал!")
            break

        if player.health <= 35 and player.heals_left() > 0:
            restored = player.heal()
            print(f"Игрок исцелился на {restored} HP")

        hit, dmg = goblin.attack_target(player)
        print("Гоблин атакует:", "попал" if hit else "промах", f"урон {dmg}" if dmg else "")
        if not player.is_alive():
            print("Игрок погиб!")
            break
        round_no += 1
