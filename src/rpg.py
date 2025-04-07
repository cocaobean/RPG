import entities
import random
import time

'''
MC has inventory "inventory" : [1,2,3] 
different uses of items
Shop.
choice of opening inventory every round
while in batttle : item, and different atk, and spells
'''

def shop(player: entities.Player):
    # TODO: add more stuf to the shop, make on_sale a list so there are multiple things on sale
    print("Welcome to the shop! You have", player.money, "dollars.", "This is what's on sale today.")
    stock = [("1. Healing Potions", 20), ("2. Max Health Potions", 30), ("3. Strength Potions", 20)]
    randInt = random.randint(0,2)
    on_sale = stock[randInt]
    while True:
        #TODO: make sure that game dosn't error when they put in a letter
        print("How much", on_sale[0], ", for", on_sale[1], "dollars each, would you like to buy?")
        amount = input()
        if amount.isnumeric():
            amount = int(amount)
            if player.money >= amount * int(on_sale[1]) and amount >= 0:
                player.money -= amount * int(on_sale[1])
                player.inventory[randInt][1] += amount
            else:
                print("You're too poor.")
            print("You have", player.money, "dollars left.")
            player.print_inventory()
            leave = input("Do You want to leave? (y,n)").lower()
            if leave == "y":
                print("Thank you for shopping!")
                break
        else:
            print("Please Enter an Integer.")
            
def use_item(item_chosen):
    pass
    # TODO: add what happens when you use an item.

def print_status(player: entities.Player, enemy: entities.Enemy) -> None:
    print(player.name, "has", player.health, "health")
    print(enemy.name, "has", enemy.health, "health")

def player_attack(player: entities.Player, enemy: entities.Enemy) -> bool:
    enemy.health -= player.attack
    print("You dealt", player.attack,"damage. The enemie has",enemy.health,"health left.")
    if enemy.health <= 0:
        player.xp += enemy.xp
        player.money += enemy.money
        print("You have defeated",enemy.name,". You gained", enemy.xp , "XP, and",enemy.money, "dollars.")
        return True
    else:
        return False

def enemy_attack(player: entities.Player, enemy: entities.Enemy) -> bool:
    player.health -= enemy.attack
    print(enemy.name,"dealt", enemy.attack,"damage. You have",player.health,"health left.")
    if player.health <= 0:
        print("You have been defeated by",enemy.name,".")
        print("GAME OVER")
        return True
    else:
        return False

def fight(player: entities.Player, enemy: entities.Enemy) -> None:
    print("A wild", enemy.name, "appears!")
    print() # for formatting

    while player.health > 0 and enemy.health > 0:
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
            # print(player.inventory)
            player.print_inventory()
            # for item in player.inventory:
            #     print(item[0] + " : " + item[1])
            item_chosen = input("What item to you want to use?")
            use_item(item_chosen)
            # if item_chosen == ""
        else:
            print("Invalid choice. Try again.")

def level_up(player: entities.Player) -> None:
    print("You leveled up! Do you want to increase:")
    choice = input("Strength or Max Health? (S),(MH)").lower()
    player.level += 1
    player.xp = 0
    if choice == "mh":
        player.max_health = int(player.max_health * 1.5)
    elif choice == "s":
        player.attack = int(player.attack * 1.5)
        
         

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

name = input("What is your name? ")
player1 = entities.Player(name=name)

while True:
    enemy = entities.get_random_enemy(player1)
    fight(player1, enemy)
    if player1.health <= 0:
        print("Game Over!")
        break
    elif player1.xp >= player1.level * 3:
        level_up(player1)
    shop(player1)

# Contact: Kevi.M.CECS@outlook.com
