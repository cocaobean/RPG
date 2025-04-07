import entities
import random
import time

'''
MC has inventory "inventory" : dict[str, int]
different uses of items
Shop.
choice of opening inventory every round
while in batttle : item, and different atk, and spells
'''

def shop(player: entities.Player):
    print(f"\nWelcome to the shop! You have {player.money} dollars.")
    # Define items available in the shop with their prices
    stock = {
        "Healing Potion": 20,
        "Max Health Potion": 30,
        "Strength Potion": 25 # Example price
    }
    # Simple approach: Offer one random item type per visit for now
    available_item_name = random.choice(list(stock.keys()))
    item_price = stock[available_item_name]

    print(f"Today's offer: {available_item_name} for {item_price} dollars each.")

    while True:
        amount_str = input(f"How many {available_item_name} would you like to buy? (Enter 0 or leave blank to cancel) ")
        if not amount_str: # Handle empty input
            amount = 0
        elif amount_str.isdigit():
            amount = int(amount_str)
        else:
            print("Please enter a valid number.")
            continue

        if amount < 0:
            print("Cannot buy a negative amount.")
            continue
        elif amount == 0:
            print("No purchase made.")
            break # Exit purchase loop for this item

        cost = amount * item_price
        if player.money >= cost:
            player.money -= cost
            # Add item to inventory, creating the key if it doesn't exist
            player.inventory[available_item_name] = player.inventory.get(available_item_name, 0) + amount
            print(f"You bought {amount} {available_item_name}.")
            print(f"You have {player.money} dollars left.")
            player.print_inventory()
        else:
            print("You don't have enough money.")

        leave = input("Do you want to leave the shop? (y/n): ").lower()
        if leave == "y":
            print("Thank you for shopping!")
            break # Exit shop completely
        # If 'n', loop continues, potentially offering the same item again (can be improved)

def use_item(player: entities.Player):
    if not player.inventory or all(q == 0 for q in player.inventory.values()):
        print("Your inventory is empty.")
        return # Return early if inventory is empty

    player.print_inventory()
    # Create a list of usable items (items with quantity > 0) for selection
    usable_items = {i + 1: name for i, (name, quantity) in enumerate(player.inventory.items()) if quantity > 0}

    if not usable_items: # Double check after filtering
         print("You have no items to use.")
         return

    while True:
        choice_str = input("Enter the number of the item to use (or 0 to cancel): ")
        if choice_str.isdigit():
            choice = int(choice_str)
            if choice == 0:
                print("Cancelled using item.")
                return
            elif choice in usable_items:
                item_name = usable_items[choice]
                # Apply item effect
                if item_name == "Healing Potion":
                    player.health =+ 5
                    print(f"You used a Healing Potion and restored 5 health.")
                    print(f"Current health: {player.health}/{player.max_health}")
                elif item_name == "Max Health Potion":
                    increase_amount = player.max_health-player.health # Example max health increase
                    player.health += increase_amount
                    # player.health += increase_amount # Removed healing effect
                    print(f"You used a Max Health Potion! Health increased by {increase_amount}.")
                    print(f"Current health: {player.health}/{player.max_health}") # Show current health relative to new max
                elif item_name == "Strength Potion":
                    increase_amount = int(player.attack*1.5) # Example attack increase
                    player.attack += increase_amount
                    print(f"You used a Strength Potion! Attack increased by {increase_amount}.")
                    print(f"Current attack: {player.attack}")
                else:
                    print(f"Item '{item_name}' effect not implemented yet.")
                    return # Don't consume if effect unknown

                # Consume item
                player.inventory[item_name] -= 1
                if player.inventory[item_name] == 0:
                    # Optional: remove item from inventory if quantity is zero
                    # del player.inventory[item_name]
                    pass # Keep the key with 0 quantity for simplicity for now
                break # Exit loop after successful use
            else:
                print("Invalid item number.")
        else:
            print("Please enter a number.")

def print_status(player: entities.Player, enemy: entities.Enemy) -> None:
    print(f"\n{player.name}: {player.health}/{player.max_health} HP | ATK: {player.attack}")
    print(f"{enemy.name}: {enemy.health} HP | ATK: {enemy.attack}")

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

def fight(player: entities.Player, enemy: entities.Enemy) -> None: # Return bool indicating if player survived
    print(f"\nA wild {enemy.name} appears!")
    print() # for formatting

    while player.health > 0 and enemy.health > 0:
        print_status(player, enemy)
        print("1. Attack")
        print("2. Run")
        print("3. Item")
        # print("4. Spells") # Spells not implemented yet
        choice = input("What will you do? ")
        print() # for formatting

        enemy_turn_skipped = False # Flag to check if enemy should attack

        if choice == "1":
            if player_attack(player, enemy):
                return True # Enemy defeated
            # Enemy attacks only if it survived
        elif choice == "2":
            print("You attempt to run away...")
            # Simple run mechanic: 50% chance to escape
            if random.random() < 0.5:
                print("Successfully escaped!")
                return True # Player survived (escaped)
            else:
                print("Failed to escape!")
            # Enemy gets an attack if run fails
        elif choice == "3":
            use_item(player)
            # Using an item might take the player's turn, enemy still attacks
            # Or decide if using item skips enemy turn (game design choice)
            # For now, let's assume using an item takes the turn.
            enemy_turn_skipped = False # Let enemy attack after item use
        # elif choice == "4":
        #     print("Spells are not implemented yet.")
        #     enemy_turn_skipped = True # Don't penalize player for unimplemented feature
        else:
            print("Invalid choice. Try again.")
            enemy_turn_skipped = True # Don't let enemy attack on invalid input

        # Enemy attacks if it's still alive and player didn't defeat it or run away
        if enemy.health > 0 and not enemy_turn_skipped:
            if enemy_attack(player, enemy):
                return False # Player defeated

    # After loop: check who survived
    return player.health > 0


def level_up(player: entities.Player) -> None:
    player.level += 1
    # Reset XP for the new level, carrying over excess XP could be an option too
    # Keep excess XP for now:
    player.xp -= (player.level -1) * 3 # Subtract the threshold of the level just passed
    if player.xp < 0: player.xp = 0 # Ensure XP doesn't go negative

    print(f"\n*** Level Up! You reached level {player.level}! ***")
    print("Choose a stat to increase:")
    print(f"  (MH) Max Health (Current: {player.max_health})")
    print(f"  (S)  Strength (Current: {player.attack})")

    while True:
        choice = input("Enter MH or S: ").lower()
        if choice == "mh":
            increase = int(player.max_health * 0.2) + 5 # Increase by 20% + 5 (example formula)
            player.max_health += increase
            player.health += increase # Heal by the increased amount as well
            print(f"Max Health increased by {increase} to {player.max_health}.")
            print(f"Health fully restored to {player.health}/{player.max_health}.")
            break
        elif choice == "s":
            increase = int(player.attack * 0.2) + 1 # Increase by 20% + 1 (example formula)
            player.attack += increase
            print(f"Attack increased by {increase} to {player.attack}.")
            break
        else:
            print("Invalid choice. Please enter MH or S.")
    player.print_basic_stats() # Show updated stats


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
player1.print_basic_stats() # Show initial stats

game_running = True
while game_running:
    # Check for level up before the next action/fight
    level_threshold = player1.level * 3 # XP needed for next level
    if player1.xp >= level_threshold:
        level_up(player1)

    # Main game loop action choice (fight or shop or quit?)
    action = input("\nWhat do you want to do? (F)ight, (S)hop, (Q)uit: ").lower()

    if action == 'f':
        enemy = entities.get_random_enemy(player1)
        if not fight(player1, enemy): # fight returns False if player died
            print("\nGame Over!")
            game_running = False
    elif action == 's':
        shop(player1)
    elif action == 'q':
        print("\nThanks for playing!")
        game_running = False
    else:
        print("Invalid action. Choose F, S, or Q.")


# Contact: Kevi.M.CECS@outlook.com
