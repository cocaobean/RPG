import random
import time

# TODO: Convert character dictionary templates into objects

# TODO: Maybe implement difiiculty levels that change the player/enemy stats
player = {
  "name": "Player",    # default name
  "max health": 20,
  "health": 20,
  "attack": 2,
  "level": 1,
  "xp": 0,
  "money" : 0,
  "inventory" : [["1. Healing Potion", 2], 
                 ["2. Max Health Potion", 0],
                 ["3. Strength Potion", 1]]
}


# TODO: different enemies have different xp increase
enemy_1 = {
  "name": "Blob",
  "description": "This guy is super duper evil.",
  "health": 6,
  "attack": 2,
  "xp": 5,
  "money" : 5,
}

enemy_2 = {
  "name": "Slime",
  "description": "Man I hate this guy.",
  "health": 6,
  "attack": 3,
  "xp": 6,
  "money" : 6
}

enemy_3 = {
  "name": "Metal Cube",
  "description": "NOOO!!! Not him again.",
  "health": 10,
  "attack": 1,
  "xp" : 5,
  "money" : 5
}

enemy_4 = {
  "name": "Ogre",
  "description": "That sword looks big",
  "health": 5,
  "attack": 6,
  "xp" : 7,
  "money" : 7
}

enemies = [enemy_1, enemy_2, enemy_3, enemy_4]

'''
MC has inventory "inventory" : [1,2,3] 
different uses of items
Shop.
choice of opening inventory every round
while in batttle : item, and different atk, and spells
'''

def shop():
    # TODO: add more stuf to the shop, make on_sale a list so there are multiple things on sale
    print("Welcome to the shop! You have", player["money"], "dollars.", "This is what's on sale today.")
    stock = [("1. Healing Potion", 20), ("2. Max Health Potion", 30), ("3. Strength Potion", 20)]
    randInt = random.randint(0,2)
    on_sale = stock[randInt]
    while True:
        print("How much", on_sale[0], "would you like to buy?")
        amount = int(input())
        if player["money"] >= amount * int(on_sale[1]) and amount >= 0:
            player["money"] -= amount * int(on_sale[1])
            player["inventory"][randInt][1] += amount
        else:
            print("You're too poor.")
        print("You have", player["money"], "dollars left.")
        for i in range(len(player["inventory"])):
                if player["inventory"][i][1] > 0:
                    print(player["inventory"][i][0], ":", str(player["inventory"][i][1]), "left")
        leave = input("Do You want to leave? (y,n)").lower()
        if leave == "y":
            print("Thank you for shopping!")
            break
            
def use_item(item_chosen):
    pass
    # TODO: add what happens when you use an item.
    
    

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
        player["money"] += enemy["money"]
        print("You have defeated",enemy["name"],". You gained", enemy["xp"] , "XP, and",enemy["money"], "dollars.")
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
        print("3. Item")
        print("4. Spells")
        choice = input("What will you do? ")
        print() # for formatting

        if choice == "1":
            if player_attack(player, enemy):
                break
            if enemy_attack(player, enemy):
                break
        elif choice == "2":
            print("You run away...")
            enemy_attack(player, enemy)
            break
        elif choice == "3":
            # print(player["inventory"])
            for i in range(len(player["inventory"])):
                if player["inventory"][i][1] > 0:
                    print(player["inventory"][i][0], ":", str(player["inventory"][i][1]), "left")
            # for item in player["inventory"]:
            #     print(item[0] + " : " + item[1])
            item_chosen = input("What item to you want to use?")
            use_item(item_chosen)
            # if item_chosen == ""
        else:
            print("Invalid choice. Try again.")

def level_up(player: dict) -> None:
    print("You leveled up! Do you want to increase:")
    choice = input("Strength or Max Health? (S),(MH)").lower()
    player["level"] += 1
    player["xp"] = 0
    if choice == "mh":
        player["max health"] = int(player["max health"] * 1.5)
    elif choice == "s":
        player["attack"] = int(player["attack"] * 1.5)
         

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
    shop()
