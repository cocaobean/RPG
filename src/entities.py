import random
from typing import Dict

class Entity:
    def __init__(
        self,
        name: str,
        health: int,
        attack: int,
        xp: int,
        money: int
    ):
        self.name = name
        self.health = health
        self.attack = attack
        self.xp = xp
        self.money = money

    def print_basic_stats(self) -> None:
        print(f"{self.name}:")
        print(f"Health: {self.health}")
        print(f"Attack: {self.attack}")
        print(f"XP: {self.xp}")
        print(f"Money: {self.money}")

# Inherit print_basic_stats() and generic parameters from Entity
class Player(Entity):
    def __init__(
        self,
        name: str = "Player",
        health: int = 20,
        attack: int = 2,
        level: int = 1,
        xp: int = 0,
        money: int = 0,
        inventory: Dict[str, int] = {
            "Healing Potion": 2,
            "Max Health Potion": 1,
            "Strength Potion": 1
        }
    ):
        super().__init__(name, health, attack, xp, money)
        self.level = level
        self.max_health = health # Initialize max_health
        self.inventory = inventory

    def print_inventory(self) -> None:
        print("Inventory:")
        if not self.inventory:
            print("  Empty")
            return
        # Enumerate to provide numbers for selection
        for i, (item, quantity) in enumerate(self.inventory.items()):
            if quantity > 0:
                print(f"  {i + 1}. {item}: {quantity}")

class Enemy(Entity):
    def __init__(
        self,
        name: str = "Enemy",
        health: int = random.randint(1, 10),
        attack: int = random.randint(1, 5),
        xp: int = random.randint(1, 10),
        money: int = random.randint(1, 10)
    ):
        super().__init__(name, health, attack, xp, money)

class Slime(Entity):
    def __init__(
        self,
        health: int = random.randint(3, 5),
        attack: int = random.randint(2, 4),
        xp: int = random.randint(2,3 ),
        money: int = random.randint(2, 4)
    ):
        super().__init__("Slime", health, attack, xp, money)

class Iron_Cube(Entity):
    def __init__(
        self,
        health: int = random.randint(9, 12),
        attack: int = random.randint(1, 2),
        xp: int = random.randint(5, 6),
        money: int = random.randint(5, 7)
    ):
        super().__init__("Iron Cube", health, attack, xp, money)

class Ogre(Entity):
    def __init__(
        self,
        health: int = random.randint(4, 6),
        attack: int = random.randint(3, 5),
        xp: int = random.randint(5, 6),
        money: int = random.randint(5, 6)
    ):
        super().__init__("Ogre", health, attack, xp, money)

def get_random_enemy(player: Player) -> Entity:
    # Use player level to potentially scale enemies or select different ones
    if player.level > 10: # Example: harder enemies for higher levels
        enemies = [Iron_Cube(), Ogre()] # Add potentially harder enemies later
    elif player.level > 5:
         enemies = [Slime(), Iron_Cube(), Ogre()]
    else:
        enemies = [Slime(), Iron_Cube()] # Start with easier enemies
    return random.choice(enemies)

# Testing single file entities.py
if __name__ == "__main__":
    entity = Entity("Generic NPC", 10, 1, 1, 0)
    entity.print_basic_stats()
    
    player = Player()
    player.print_basic_stats()
    print(f"Max Health: {player.max_health}") # Test max_health
    player.print_inventory()
    
    slime = Slime()
    slime.print_basic_stats()
    
    iron_cube = Iron_Cube()
    iron_cube.print_basic_stats()
    
    ogre = Ogre()
    ogre.print_basic_stats()
    
    # Pass player object to get_random_enemy
    enemy = get_random_enemy(player)
    enemy.print_basic_stats()