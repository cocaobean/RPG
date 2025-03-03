import random
import time


# TODO: Maybe implement difiiculty levels that change the player/enemy stats
player = {
  "name": "Player",    # default name
  "max health": 20,
  "health": 20,
  "attack": 2,
  "level": 1,
  "xp": 0
}

# TODO: different enemies have different xp increase
enemy_1 = {
  "name": "Blob",
  "description": "This guy is super duper evil.",
  "health": 6,
  "attack": 2,
  "xp": 5,
}

enemy_2 = {
  "name": "Slime",
  "description": "Man I hate this guy.",
  "health": 6,
  "attack": 3,
  "xp": 6
}

enemy_3 = {
  "name": "Metal Cube",
  "description": "NOOO!!! Not him again.",
  "health": 10,
  "attack": 1,
  "xp" : 5
}

enemy_4 = {
  "name": "Ogre",
  "description": "That sword looks big",
  "health": 5,
  "attack": 6,
  "xp" : 7
}

enemies = [enemy_1, enemy_2, enemy_3, enemy_4]

def get_enemy() -> dict:
    return enemies[random.randint(0, len(enemies) - 1)].copy()

def print_status(player: dict, enemy: dict) -> None:
    print(player["name"], "has", player["health"], "health")
    print(enemy["name"], "has", enemy["health"], "health")

def player_attack(player: dict, enemy: dict) -> bool:
    enemy["health"] -= player["attack"]
    print("You dealt", player["attack"],"damage. The enemie has",enemy["health"],"health left.")
    if enemy["health"] <= 0:
        player["xp"] += enemy["xp"]
        print("You have defeated",enemy["name"],". You gained", enemy["xp"] , "XP.")
        return True
    else:
        return False

def enemy_attack(player: dict, enemy: dict) -> bool:
    player["health"] -= enemy["attack"]
    print(enemy["name"],"dealt", enemy["attack"],"damage. You have",player["health"],"health left.")
    if player["health"] <= 0:
        print("You have been defeated by",enemy["name"],".")
        print("GAME OVER")
        return True
    else:
        return False

def fight(player: dict, enemy: dict) -> None:
    print("A wild", enemy['name'], "appears!")
    print(enemy["description"])
    print() # for formatting

    while player['health'] > 0 and enemy['health'] > 0:
        print_status(player, enemy)
        print("1. Attack")
        print("2. Run")
        choice = input("What will you do? ")
        print() # for formatting

        if choice == "1":
            if player_attack(player, enemy):
                break
            if enemy_attack(player, enemy):
                break
        elif choice == "2":
            print("You run away...")
            break
        else:
            print("Invalid choice. Try again.")

def level_up(player: dict) -> None:
    print("You leveled up! Do you want to increase:")
    choice = input("Strength or Max Health? (S),(MH)").lower()
    if choice == "mh":
        player["max health"] = player["max health"] * 1.2
    elif choice == "s":
        player["attack"] = player["attack"] * 1.2
         

# Custom intro:
user_input = input("Welcome explorer, are you ready to explore the dungeon? (Y)(N): ").upper()
if user_input == "Y":
    print("Good, I see that you are excited!")
else:
    print("HOW DARE YOU SAY NO!!!")
    time.sleep(2)
    for i in range(100):
        print('''||||||||||||||||||||||||||||||||||||||||||||||||||||||''')
        time.sleep(0.1)
    print("GAME OVER HOW DARE YOU CHOOSE NO!!! You will be traped in the endless cycle of ||||||||||||")
    time.sleep(5)
    while True:
        print('''||||||||||||||||||||||||||||||||||||||||||||||||||||||''')
        time.sleep(0.1)

player["name"] = input("What is your name? ")

while True:
    enemy = get_enemy()
    fight(player, enemy)
    if player['health'] <= 0:
        print("Game Over!")
        break
    elif player['xp'] >= player['level'] * 3:
        level_up(player)
