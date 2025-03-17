class Player:
    def __init__(
            self,
            name: str = "Player",
            max_health: int = 20,
            health: int = 20,
            attack: int = 2,
            level: int = 1,
            xp: int = 0,
            money: int = 0,
            inventory: list[list] = [
                    ["1. Healing Potion", 2], 
                    ["2. Max Health Potion", 1],
                    ["3. Strength Potion", 1]
                ]
            ):
        self.name = name
        self.max_health = max_health
        self.health = health
        self.attack = attack
        self.level = level
        self.xp = xp
        self.money = money
        self.inventory = inventory

    def print_inventory(self) -> None:
        for item, quantity in self.inventory:
            if quantity == 0:
                continue    # skip

            print(item, ":", str(quantity), "left")