import random

class Enemy:
    def __init__(
            self,
            name: str = "Enemy",
            health: int = 5,
            attack: int = 5,
            level: int = 5,
            xp: int = 5,
            money: int = 5
            ):
        self.name = name
        self.health = health
        self.attack = attack
        self.level = level
        self.xp = xp
        self.money = money