import sys
import time
import random
import json
import os
import msvcrt

DOWNLOADS_FOLDER = os.path.join(
    os.path.expanduser("~"),
    "Downloads"
)

SAVE_FILE = os.path.join(
    DOWNLOADS_FOLDER,
    "save.json"
)

rarity_chances = {
    "common": 70,
    "uncommon": 22.3,
    "rare": 5.4,
    "epic": 2,
    "legendary": 0.3
}

bash_times = 0
lash_times = 0
mash_times = 0

dead_sector_unlocked = False

fortress_progress = 0
fortress_completed = False

throw_mountain = 0

shatter_times = 0

rock_speedrun = False

multi_boulder = 0
throw_boulder = 0

player_x = 0
player_y = 4

old_x = player_x
old_y = player_y

width = 10
height = 5

enemies_killed = 0
deaths = 0

throw_used = 0

moved = False

weapon = "Rock"

explored = [(0, 4)]

inventory = {}

money = 50

health_upgrades = 0
restores = 0

thrust_times = 0

seen_enemies = set()

wooden_sword = False
throw_rock_multi = 0
slice_times = 0
stone_stab = 0

camp_progress = 0
camp_completed = False

new_zone_unlocked = False

zone = "Plains"

def animation(text, speed=0.09, cycles=3):

    for i in range(cycles * 4):

        dots = "." * (i % 4)

        sys.stdout.write("\r" + " " * 50)
        sys.stdout.write("\r")
        sys.stdout.write(text + dots)
        sys.stdout.flush()

        time.sleep(speed)

    print()

def rock_speedruns():
    global rock_speedrun
    global weapon
    if rock_speedrun == False:
        rock_speedrun = True
        weapon = "Rock"
        print("Rock speedrun ON")
    elif rock_speedrun == True:
        rock_speedrun = False
        print("Rock speedrun OFF")


    

def save_game():

    filename = SAVE_FILE

    data = {
        "player_name": player.name,
        "health": player.health,
        "max_health": player.max_health,
        "player_x": player_x,
        "player_y": player_y,
        "enemies_killed": enemies_killed,
        "deaths": deaths,
        "weapon": weapon,
        "inventory": inventory,
        "money": money,
        "health_upgrades": health_upgrades,
        "restores": restores,
        "explored": explored,
        "seen_enemies": list(seen_enemies),
        "wooden_sword": wooden_sword,
        "camp_completed": camp_completed,
        "new_zone_unlocked": new_zone_unlocked,
        "zone": zone,
        "fortress_completed": fortress_completed,
        "dead_sector_unlocked": dead_sector_unlocked,

    }

    try:

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        print()
        print("GAME SAVED!")
        print()
        print("Your save file is:")
        print(filename)
        print()

    except Exception as e:

        print()
        print("SAVE FAILED!")
        print(e)
        print()


def load_game():

    global player_x, player_y
    global enemies_killed, deaths
    global weapon, inventory, money
    global health_upgrades, restores
    global explored, seen_enemies
    global wooden_sword
    global camp_completed, new_zone_unlocked
    global zone
    global fortress_completed
    global dead_sector_unlocked

    filename = SAVE_FILE

    if not os.path.exists(filename):

        print()
        print("NO SAVE FILE FOUND!")
        print()
        print("Looking for:")
        print(filename)
        print()

        return

    try:

        with open(filename, "r") as f:
            data = json.load(f)

        player.name = data["player_name"]
        player.health = data["health"]
        player.max_health = data["max_health"]

        player_x = data["player_x"]
        player_y = data["player_y"]

        enemies_killed = data["enemies_killed"]
        deaths = data["deaths"]

        weapon = data["weapon"]
        inventory = data["inventory"]
        money = data["money"]

        health_upgrades = data["health_upgrades"]
        restores = data["restores"]

        explored = [tuple(pos) for pos in data["explored"]]
        seen_enemies = set(data["seen_enemies"])

        wooden_sword = data["wooden_sword"]

        camp_completed = data["camp_completed"]
        new_zone_unlocked = data["new_zone_unlocked"]

        zone = data["zone"]

        fortress_completed = data["fortress_completed"]

        dead_sector_unlocked = data["dead_sector_unlocked"]

        print()
        print("GAME LOADED!")
        print()
        print(f"Welcome back, {player.name}.")
        print(f"Money: ${money}")
        print(f"HP: {player.health}/{player.max_health}")
        print(f"Weapon: {weapon}")
        print(f"Zone: {zone}")
        print()

    except Exception as e:

        print()
        print("LOAD FAILED!")
        print(e)
        print()

def clear_input():
    while msvcrt.kbhit():
        msvcrt.getwch()

def typewriter(text, speed=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()


def typewriter1(text, speed=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)


def show_map():

    grid = [['?' for _ in range(width)] for _ in range(height)]

    for x, y in explored:
        grid[y][x] = '.'

    if zone == "Plains":

        grid[2][3] = 'W'
        grid[4][1] = 'S'
        grid[2][7] = 'E'
        grid[2][8] = '>'
        grid[4][9] = 'F'

        print("____________ THE PLAINS ____________")

    elif zone == "Wastelands":

        grid[2][0] = '<'
        grid[2][5] = 'W'
        grid[1][8] = 'S'
        grid[3][3] = 'F'
        grid[2][9] = '>'

        print("__________ THE WASTELANDS __________")

    elif zone == "Dead Sector":

            grid[2][0] = '<'
            grid[3][5] = 'W'
            grid[3][2] = 'S'

            print("__________ THE DEAD SECTOR __________")


    grid[player_y][player_x] = 'P'

    for row in grid:
        print(" ".join(row))
    print()


def workshop():

    global wooden_sword, weapon

    while True:

        print("_____ WORKSHOP _____")
        print()

        typewriter(
            "Hey, welcome in! Got some materials? Let's see what we can make.",
            speed=0.02
        )

        print("[1] Craft")
        print("[2] Leave")

        choice = input("> ")

        if choice == "1" and not wooden_sword:

            print()
            print("_____ CRAFTING _____")
            print()

            print("[1] Wooden Sword")
            print("[2] Back")

            choice = input("> ")

            if choice == "1":

                if inventory.get("Wood", 0) >= 3 and inventory.get("Leather", 0) >= 1:

                    print()
                    print("Materials:")
                    print("Wood: 3")
                    print("Leather: 1")
                    print()

                    typewriter("Crafting...", speed=0.05)
                    time.sleep(3.2)

                    inventory["Wood"] -= 3
                    inventory["Leather"] -= 1

                    weapon = "Wooden Sword"
                    wooden_sword = True

                    print()
                    typewriter("You crafted a Wooden Sword!")
                    print("Weapon equipped: Wooden Sword")

                else:

                    print()
                    print("You don't have the materials.")
                    print("You need 3 Wood and 1 Leather.")

            elif choice == "2":

                print()

            else:

                print("Not an option.")

        elif choice == "1" and wooden_sword:

            print()
            print("_____ CRAFTING _____")
            print("[1] Stone Sword")
            print("[2] Back")

            choice = input("> ")

            if choice == "2":
                print()

            elif choice == "1":
                if inventory.get("Stone", 0) >= 5 and inventory.get("Leather", 0) >= 2:
                    print()
                    print("Materials:")
                    print("Stone: 5")
                    print("Leather: 2")
                    print()

                    typewriter("Crafting...", speed=0.05)
                    time.sleep(5.9)
                    inventory["Stone"] -= 5
                    inventory["Leather"] -= 2

                    weapon = "Stone Sword"

                    typewriter("You crafted a Stone Sword!")
                    typewriter("Weapon equipped: Stone Sword")

                else:
                    print()
                    print("You don't have the materials.")
                    print("You need 5 Stone and 2 Leather.")


        elif choice == "2":

            typewriter(
                "Already leaving? Alright, come back when you find something worth building.",
                speed=0.02
            )

            break

        if weapon == "Stone Sword":
            print("[1] Iron Sword")
            print("[2] Back")
            choice = input("> ")
            if choice == "1":
                if inventory.get("Iron", 0) >= 5 and inventory.get("Strap", 0) >= 3:
                    print()
                    print("Materials:")
                    print("Iron: 5")
                    print("Strap: 3")
                    print()
                    typewriter("Crafting...")
                    time.sleep(3)
                    inventory["Iron"] -= 5
                    inventory["Strap"] -= 3
                    weapon = "Iron Sword"
                    typewriter("You crafted an Iron Sword!")
                    typewriter("Weapon equipped: Iron Sword")

                else:
                    print("You don't have the materials.")
                    print("You need 5 Iron and 3 Straps.")
        else:

            typewriter(
                "Not sure what you mean. Try one of the options.",
                speed=0.02
            )


def shop():

    global money, health_upgrades, restores

    while True:

        print("_____ SHOP _____")

        typewriter(
            "Oh great. You again, what d'ya need?",
            speed=0.02
        )

        print()
        print(f"Money: ${money}")
        print(f"HP: {player.health}/{player.max_health}")
        print()

        print("[1] Buy Health")
        print("[2] Sell Drops")
        print("[3] Health")
        print("[4] Leave")

        choice = input("> ")

        if choice == "1":

            health_price = 25 + (health_upgrades * 15)

            print()
            print("Health upgrade: +10 max HP")
            print(f"Cost: ${health_price}")

            if money >= health_price:

                money -= health_price
                health_upgrades += 1

                player.max_health += 10
                player.health = player.max_health

                print("There. More health.")
                print(f"Max HP: {player.max_health}")
                print(f"Money: ${money}")

            else:

                print("You can't afford that.")

        elif choice == "2":

            while True:

                print()
                print("_____ SELL DROPS _____")
                print(f"Money: ${money}")
                print()

                print(f"[1] Wood - ${inventory.get('Wood', 0)}")
                print(f"[2] Leather - ${inventory.get('Leather', 0)}")
                print(f"[3] Rope - ${inventory.get('Rope', 0)}")
                print("[4] Back")

                sell_choice = input("> ")

                if sell_choice == "1":

                    if inventory.get("Wood", 0) > 0:

                        inventory["Wood"] -= 1
                        money += 3

                        print("You sold 1 Wood for $3.")

                    else:

                        print("You don't have any Wood.")

                elif sell_choice == "2":

                    if inventory.get("Leather", 0) > 0:

                        inventory["Leather"] -= 1
                        money += 8

                        print("You sold 1 Leather for $8.")

                    else:

                        print("You don't have any Leather.")

                elif sell_choice == "3":

                    if inventory.get("Rope", 0) > 0:

                        inventory["Rope"] -= 1
                        money += 6

                        print("You sold 1 Rope for $6.")

                    else:

                        print("You don't have any Rope.")

                elif sell_choice == "4":

                    break

                else:

                    print("That's not an option.")

        elif choice == "3":

            while True:

                print()
                print("_____ HEALTH _____")
                print(f"HP: {player.health}/{player.max_health}")
                print()

                print("[1] Heal 10 HP - $8")
                print("[2] Heal 50 HP - $30")

                restore_price = 50 + (restores * 15)

                print(f"[3] Restore Full Health - ${restore_price}")

                print("[4] Back")

                health_choice = input("> ")

                if health_choice == "1":

                    if player.health >= player.max_health:

                        print("You're already at full health.")

                    elif money >= 8:

                        money -= 8

                        player.health = min(
                            player.max_health,
                            player.health + 10
                        )

                        print("There. That's something.")
                        print(f"HP: {player.health}/{player.max_health}")
                        print(f"Money: ${money}")

                    else:

                        print("You can't afford that.")

                elif health_choice == "2":

                    if player.health >= player.max_health:

                        print("You're already at full health.")

                    elif money >= 30:

                        money -= 30

                        player.health = min(
                            player.max_health,
                            player.health + 50
                        )

                        print("That should keep you going.")
                        print(f"HP: {player.health}/{player.max_health}")
                        print(f"Money: ${money}")

                    else:

                        print("You can't afford that.")

                elif health_choice == "3":

                    if player.health >= player.max_health:

                        print("You're already at full health.")

                    elif money >= restore_price:

                        money -= restore_price
                        restores += 1

                        player.health = player.max_health

                        print("There. Good as new.")
                        print(f"HP: {player.health}/{player.max_health}")
                        print(f"Money: ${money}")

                    else:

                        print("You can't afford that.")

                elif health_choice == "4":

                    break

                else:

                    print("That's not an option.")

        elif choice == "4":

            typewriter(
                "Finally, now get outta here.",
                speed=0.02
            )

            break

        else:

            print(
                "What the hell is that supposed to mean? "
                "Pick something from the damn menu."
            )


def combat(enemy):

    global enemies_killed, deaths, money
    global throw_used, throw_rock_multi
    global stone_stab, slice_times, throw_boulder, multi_boulder
    global thrust_times
    global shatter_times
    global throw_mountain
    global mash_times, lash_times, bash_times

    slice_times = 0
    stone_stab = 0

    throw_used = 0
    throw_rock_multi = 0

    throw_boulder = 0
    multi_boulder = 0
    
    thrust_times = 0
    shatter_times = 0
    throw_mountain = 0

    mash_times = 0
    lash_times = 0
    bash_times = 0

    while player.health > 0 and enemy.health > 0:

        print()
        print(f"HP: {player.health}")
        print(f"Enemy HP: {enemy.health}")
        print()

        if weapon == "Rock":

            print("[1] Hit with rock")

            if enemies_killed >= 5:

                print("[2] Throw Rock")

                if enemies_killed >= 10:

                    print("[3] Throw multiple rocks")

                    if enemies_killed >= 50:
                        print("[4] Throw boulder")
                        if enemies_killed >= 100:
                            print("[5] Throw multiple boulders.")
                            if enemies_killed >= 125:
                                print("[6] Throw Mountain")

            if not rock_speedrun:
                clear_input()
            option = input("> ")


            if option == "6" and enemies_killed >= 125:
                if throw_mountain == 1:
                    print("You have already thrown a mountain...")
                else:
                    player.attack = random.randint(32, 49)

                    animation("Throwing mountain")

                    enemy.health -= player.attack
                    throw_mountain += 1
                    print()
                    print(f"You dealt {player.attack} damage!")
                    print(
                        f"{enemy.name} health: "
                        f"{max(0, enemy.health)}"
                    )


            elif option == "5" and enemies_killed >= 100:
                if multi_boulder == 3:
                    print("You should be glad that I allowed you to use super strength.")
                else:
                    player.attack = random.randint(29, 42)

                    animation("Throwing boulders")

                    enemy.health -= player.attack

                    print()
                    print(f"You dealt {player.attack} damage!")
                    print(
                        f"{enemy.name} health: "
                        f"{max(0, enemy.health)}"
                    )

            elif option == "1":

                player.attack = random.randint(3, 7)

                animation("Hitting with rock", speed = 0.09)


                enemy.health -= player.attack

                print()
                print(f"You dealt {player.attack} damage!")
                print(
                    f"{enemy.name} health: "
                    f"{max(0, enemy.health)}"
                )

            elif option == "2" and enemies_killed >= 5:

                if throw_used == 5:

                    print(
                        "You have thrown too much rocks "
                        "in this battle."
                    )

                    continue

                else:

                    animation("Throwing rock")

                    player.attack = random.randint(4, 8)

                    enemy.health -= player.attack

                    print()
                    print(f"You dealt {player.attack} damage!")
                    print(
                        f"{enemy.name} health: "
                        f"{max(0, enemy.health)}"
                    )

                    throw_used += 1

            elif option == "3" and enemies_killed >= 10:

                if throw_rock_multi == 3:

                    print(
                        "You have thrown too many rocks."
                    )

                    continue

                else:

                    animation("Throwing rocks")

                    player.attack = random.randint(7, 12)

                    enemy.health -= player.attack

                    print()
                    print(f"You dealt {player.attack} damage!")
                    print(
                        f"{enemy.name} health: "
                        f"{max(0, enemy.health)}"
                    )

                    throw_rock_multi += 1

            elif option == "4" and enemies_killed >= 50:
                if throw_boulder == 1:
                    print("You have already thrown a boulder, are you crazy?")
                    continue
                else:
                    animation("Throwing boulder")
                    player.attack = random.randint(15, 22)
                    enemy.health -= player.attack
                    throw_boulder +=1
                    print()
                    print(f"You dealt {player.attack} damage!")
                    print(
                        f"{enemy.name} health: "
                        f"{max(0, enemy.health)}"
                        )

            else:

                print("That's not an option.")
                continue

        elif weapon == "Wooden Sword":

            print("[1] Slice")

            if enemies_killed >= 40:

                print("[2] Slash")

                if enemies_killed >= 75:

                    print("[3] Thrust")

            option = input("> ")

            if option == "1":

                animation("Slicing")

                player.attack = random.randint(9, 19)

                enemy.health -= player.attack

                print()
                print(f"You dealt {player.attack} damage!")
                print(
                    f"{enemy.name} health: "
                    f"{max(0, enemy.health)}"
                )

            elif option == "2" and enemies_killed >= 40:
                if slice_times >= 3:
                    print("You have slashed too much times in this battle. You are too exhausted.")
                    continue
                else:


                    animation("Slashing")
                    slice_times +=1
                    player.attack = random.randint(15, 29)

                    enemy.health -= player.attack

                    print()
                    print(f"You dealt {player.attack} damage!")
                    print(
                        f"{enemy.name} health: "
                        f"{max(0, enemy.health)}"
                    )
            elif option == "3" and enemies_killed >= 75:
                if thrust_times == "3":
                    print("You have thrusted yourself too much times.")
                    print("For some reason you have a bump on your head.")
                    continue
                else:
                    animation("Thrusting")
                    thrust_times += 1
                    player.attack = random.randint(17, 34)

                    enemy.health -= player.attack

                    print()
                    print(f"You dealt {player.attack} damage!")
                    print(
                        f"{enemy.name} health: "
                        f"{max(0, enemy.health)}"
                    )

        elif weapon == "Stone Sword":
            print("[1] Swipe")
            if enemies_killed >= 65:
                print("[2] Crash")
                if enemies_killed >= 150:
                    print("[3] Shatter")
                    if enemies_killed >= 200:
                        print("[4] Annihilate")

            option = input("> ")

            if option == "4" and enemies_killed >= 200:
                player.attack = random.randint(50, 59)
                animation("Annihilating")
                enemy.health -= player.attack
                print()
                print(f"You dealt {player.attack} damage!")
                print(
                    f"{enemy.name} health: "
                    f"{max(0, enemy.health)}"
                )

            elif option == "3" and enemies_killed >= 150:
                if shatter_times == 5:
                    print("You feel shattered. You can't do it anymore.")
                    continue
                else:
                    animation("Shattering")
                    player.attack = random.randint(32, 45)

                enemy.health -= player.attack
                shatter_times += 1

                print()
                print(f"You dealt {player.attack} damage!")
                print(
                    f"{enemy.name} health: "
                    f"{max(0, enemy.health)}"
                )
                    

            elif option == "1":
                animation("Swiping...")
                player.attack = random.randint(12, 19)

                enemy.health -= player.attack

                print()
                print(f"You dealt {player.attack} damage!")
                print(
                    f"{enemy.name} health: "
                    f"{max(0, enemy.health)}"
                )
            elif option == "2":
                if enemies_killed < 65 or stone_stab == 5:
                    print("You cannot use this move in this battle.")
                    continue
                else:
                    animation("Crashing")

                    player.attack = random.randint(29, 38)

                    enemy.health -= player.attack
                    stone_stab +=1

                    print()
                    print(f"You dealt {player.attack} damage!")
                    print(
                        f"{enemy.name} health: "
                        f"{max(0, enemy.health)}"
                    )
                    


            else:

                print("That's not an option.")
                continue


        elif weapon == "Iron Sword":
            print("[1] Smash")
            if enemies_killed >= 200:
                print("[2] Mash")
                if enemies_killed >= 250:
                    print("[3] Lash")
                    if enemies_killed >= 300:
                        print("[4] Bash")
                

            choice = input("> ")

            if choice == "1":
                animation("Smashing")
                player.attack = random.randint(32, 45)
                enemy.health -= player.attack


                print()
                print(f"You dealt {player.attack} damage!")
                print(
                    f"{enemy.name} health: "
                    f"{max(0, enemy.health)}"
                )

            elif choice == "2" and enemies_killed >= 200:
                if mash_times == 5:
                    print("You have mashed too much times.")
                    print("If you continue mashing you will be mashed.")
                    continue
                else:
                    animation("Mashing")
                    player.attack = random.randint(48,64)
                    enemy.health -= player.attack
                    mash_times += 1
                    print()
                    print(f"You dealt {player.attack} damage!")
                    print(
                        f"{enemy.name} health: "
                        f"{max(0, enemy.health)}"
                    )

            elif choice == "3" and enemies_killed >= 250:
                if lash_times == 3:
                    print("Lashing too much times will get you mashed and lashed.")
                    continue
                else:
                    animation("Lashing")
                    player.attack = random.randint(53, 64)
                    enemy.health -= player.attack
                    lash_times += 1
                    print()
                    print(f"You dealt {player.attack} damage!")
                    print(
                        f"{enemy.name} health: "
                        f"{max(0, enemy.health)}"
                    )

            elif choice == "4" and enemies_killed >= 300:
                if bash_times == 1:
                    print("You have bashed too much times.")
                    print("Bashing too much will result in you being bashed, mashed and lashed.")
                    continue
                else:
                    animation("Bashing")
                    player.attack = random.randint(63, 72)
                    enemy.health -= player.attack
                    bash_times += 1
                    print()
                    print(f"You dealt {player.attack} damage!")
                    print(
                        f"{enemy.name} health: "
                        f"{max(0, enemy.health)}"
                    )

            else:
                print("That's not an option.")



        
        else:

            print("That's not an option.")
            continue

        

        if enemy.health <= 0:

            enemies_killed += 1

            print()

            money += enemy.money

            typewriter(
                f"You defeated the {enemy.name}!"
            )

            print(f"Enemies killed: {enemies_killed}")
            print(f"You found ${enemy.money}!")
            print(f"Money: ${money}")

            if (
                enemy.drop is not None
                and random.randint(1, 100) <= enemy.drop_chance
            ):

                inventory[enemy.drop] = (
                    inventory.get(enemy.drop, 0) + 1
                )

                print(
                    f"They dropped: {enemy.drop}!"
                )

            return True

        enemy_damage = enemy.attack

        player.health -= enemy_damage

        print()
        print(f"The {enemy.name} attacks!")
        print(f"You take {enemy_damage} damage.")

        if player.health <= 0:

            deaths += 1

            print()

            typewriter("You were defeated.")

            print(f"Deaths: {deaths}")

            player.max_health = max(
                10,
                player.max_health - 10
            )

            player.health = player.max_health

            print(
                f"Your new maximum health is "
                f"{player.max_health}."
            )

            print("You remain in this area.")

            return False


def camp():

    global camp_progress
    global camp_completed
    global new_zone_unlocked

    print()
    print("_____ ENEMY CAMP _____")
    print()

    if camp_completed:

        print("The camp has already been cleared.")
        return True

    if enemies_killed <= 25:

        typewriter("Beware.")
        typewriter("This area is not for beginners.")

        print()
        print("Recommended:")
        print("- Wooden Sword")
        print("- Lots of kills")
        print("- Plenty of money")
        print("- High maximum HP")

        print()
        print("You should get more kills.")
        print("You should probably come back later.")


    print("Beware.")
    print()

    print("This area is extremely dangerous.")
    print()

    print("Recommended:")
    print("- Wooden Sword")
    print("- Lots of kills")
    print("- Plenty of money")
    print("- High maximum HP")

    print()
    print("You will fight 5 enemies in a row.")
    print("There will be no healing between fights.")
    print("After the 5th enemy, you will be fully healed.")
    print("Then you will fight the camp boss.")

    print()

    print("[1] Enter")
    print("[2] Leave")

    if not rock_speedrun:
        clear_input()
    choice = input("> ")


    if choice != "1":

        print("You decided to leave.")
        return False

    print()

    typewriter("You enter the camp.")

    camp_progress = 0

    while camp_progress < 5:

        print()
        print(
            f"_____ CAMP FIGHT "
            f"{camp_progress + 1}/5 _____"
        )

        enemy = random.choice(all_enemies)()

        print(f"A {enemy.name} appears!")

        seen_enemies.add(enemy.name)

        won = combat(enemy)

        if not won:

            print()
            print("You were forced out of the camp.")

            camp_progress = 0

            return False

        camp_progress += 1

        print()
        print(
            f"Camp enemies defeated: "
            f"{camp_progress}/5"
        )

        if camp_progress < 5:

            typewriter(
                "Another enemy approaches..."
            )

    print()

    typewriter("The camp goes silent.")
    typewriter(
        "You have defeated all five enemies."
    )

    print()

    typewriter(
        "You take a moment to recover."
    )

    player.health = player.max_health

    print()
    print(
        f"HP restored: "
        f"{player.health}/{player.max_health}"
    )

    print()

    typewriter("But then...")
    print()

    boss = CampBossEnemy()

    print("_____ CAMP BOSS _____")
    print()

    typewriter(
        f"The {boss.name} appears!"
    )

    print()

    seen_enemies.add(boss.name)

    won = combat(boss)

    if won:

        print()

        typewriter(
            "The camp boss has been defeated."
        )

        typewriter(
            "The way forward is now open."
        )


        camp_completed = True
        new_zone_unlocked = True

        return True

    else:

        return False



def infinite_area():

    print()
    print("_____ ENDLESS GROUNDS _____")
    print()

    typewriter(
        "There is no end to the enemies here."
    )

    while True:

        enemy = random.choice(all_enemies)()

        print()
        print(f"A {enemy.name} appears!")

        seen_enemies.add(enemy.name)

        won = combat(enemy)

        if not won:

            print()
            print(
                "You leave the Endless Grounds."
            )

            break

        print()
        print("[1] Fight another")
        print("[2] Leave")

        if not rock_speedrun:
            clear_input()
        choice = input("> ")


        if choice == "2":

            break

        elif choice != "1":

            print("That's not an option.")


def choose_enemy(enemy_list):

    rarity = random.choices(
        list(rarity_chances.keys()),
        weights=list(rarity_chances.values())
    )[0]

    matching_enemies = [
        enemy for enemy in enemy_list
        if enemy().rarity == rarity
    ]

    if not matching_enemies:
        return random.choice(enemy_list)()

    return random.choice(matching_enemies)()

def move_player(new_x, new_y):

    global player_x, player_y
    global zone
    global explored

    old_x = player_x
    old_y = player_y

    # =========================
    # PLAINS
    # =========================

    if zone == "Plains":

        # Enemy Camp
        if (new_x, new_y) == (7, 2):

            won = camp()

            if won:

                player_x = new_x
                player_y = new_y

                if (new_x, new_y) not in explored:

                    explored.append(
                        (new_x, new_y)
                    )

            else:

                player_x = old_x
                player_y = old_y

        # Wastelands entrance
        elif (new_x, new_y) == (8, 2):
                
            if not new_zone_unlocked:

                print()
                print(
                    "The path ahead is blocked."
                )

                print(
                    "You must defeat the Enemy Camp first."
                )

                return False

            zone = "Wastelands"

            player_x = 1
            player_y = 2

            explored = [(1, 2)]

            print()
            print(
                "_____ THE WASTELANDS _____"
            )

            typewriter("You enter the wastelands.", speed = 0.02)
            typewriter("The first thing you notice is the heat.", speed = 0.02)
            typewriter("The second thing you notice is the lack of shade.", speed = 0.02)
            typewriter("The third thing you notice is someone is staring at you.", speed = 0.02)
            typewriter('"Oi."', speed = 0.02)
            typewriter("You turn around.", speed = 0.02)
            typewriter("A guy is standing outside a shop.")
            typewriter('"You planning on standing there all day?"', speed = 0.02)
            typewriter("...")
            typewriter("Maybe the Wastelands aren't as empty as you thought.", speed = 0.02)

        # Endless Grounds
        elif (new_x, new_y) == (9, 4):

            player_x = new_x
            player_y = new_y

            infinite_area()

        # Normal unexplored Plains tile
        elif (new_x, new_y) not in explored:

            enemy = choose_enemy(all_enemies)

            print(
                f"A {enemy.name} appears!"
            )

            seen_enemies.add(
                enemy.name
            )

            won = combat(enemy)

            if won:

                player_x = new_x
                player_y = new_y

                explored.append(
                    (new_x, new_y)
                )

                return True

            else:

                player_x = old_x
                player_y = old_y

                return False
        else:

            player_x = new_x
            player_y = new_y
            return True
    
    # =========================
    # WASTELANDS
    # =========================

    elif zone == "Wastelands":

        # Return to Plains
        if (new_x, new_y) == (0, 2):

            zone = "Plains"

            player_x = 8
            player_y = 2

            explored = [(8, 2)]

            print()
            print(
                "_____ THE PLAINS _____"
            )

            typewriter(
                "You return to the plains."
            )

            return True

        # Dead Sector entrance
        elif (new_x, new_y) == (9, 2):
                
            if not dead_sector_unlocked:

                print()
                print("The path ahead is sealed.")
                print("You must defeat the Scrap Fortress first.")

                return False

            zone = "Dead Sector"

            player_x = 1
            player_y = 2

            explored = [(1, 2)]

            print()
            print("_____ THE DEAD SECTOR _____")
            typewriter("You step past the fortress into the Dead Sector.", speed=0.02)
            typewriter("Static hums in the air. Nothing grows here.", speed=0.02)

            return True

        elif (new_x, new_y) == (3, 3):

                    won = scrap_fortress()

                    if won:

                        player_x = new_x
                        player_y = new_y

                        if (new_x, new_y) not in explored:

                            explored.append(
                                (new_x, new_y)
                            )

                    else:

                        player_x = old_x
                        player_y = old_y


    

        # Normal unexplored Wastelands tile
        elif (new_x, new_y) not in explored:

            enemy = choose_enemy(wasteland_enemies)

            print(
                f"A {enemy.name} appears!"
            )

            seen_enemies.add(
                enemy.name
            )

            won = combat(enemy)

            if won:

                player_x = new_x
                player_y = new_y

                explored.append(
                    (new_x, new_y)
                )

                return True

            else:

                player_x = old_x
                player_y = old_y

                return False

        # Already explored Wastelands tile
        else:

            player_x = new_x
            player_y = new_y

            return True

            # =========================
    # DEAD SECTOR
    # =========================

    elif zone == "Dead Sector":

        # Return to Wastelands
        if (new_x, new_y) == (0, 2):

            zone = "Wastelands"

            player_x = 8
            player_y = 2

            explored = [(8, 2)]

            print()
            print("_____ THE WASTELANDS _____")

            typewriter(
                "You return to the wastelands."
            )

            return True

        # Normal unexplored Dead Sector tile
        elif (new_x, new_y) not in explored:

            enemy = choose_enemy(dead_sector_enemies)

            print(
                f"A {enemy.name} appears!"
            )

            seen_enemies.add(
                enemy.name
            )

            won = combat(enemy)

            if won:

                player_x = new_x
                player_y = new_y

                explored.append(
                    (new_x, new_y)
                )

                return True

            else:

                player_x = old_x
                player_y = old_y

                return False

        # Already explored Dead Sector tile
        else:

            player_x = new_x
            player_y = new_y

            return True




def show_enemies():

    print("_____ ENEMIES _____")

    for enemy in all_enemies + wasteland_enemies + dead_sector_enemies:

        enemy_name = enemy().name

        if enemy_name in seen_enemies:
            print(enemy_name)
        else:
            print("???")


def show_inventory():

    print("_____ INVENTORY _____")
    print()

    if not inventory:

        print("Your inventory is empty.")

    else:
        for item, amount in inventory.items():

            print(
                f"{item} x{amount}"
            )

def scrap_fortress():
    global fortress_progress
    global fortress_completed
    global dead_sector_unlocked

    print()
    print("_____ SCRAP FORTRESS _____")
    print()

    if fortress_completed:
        print("The fortress has already been cleared.")
        return True

    print("Beware.")
    print("This zone is heavily fortified.")
    print()
    print("You will fight 5 wasteland enemies in a row.")
    print("No healing between fights until the boss.")
    print()

    print("[1] Enter")
    print("[2] Leave")

    if not rock_speedrun:
        clear_input()
    choice = input("> ")

    if choice != "1":
        print("You decided to leave.")
        return False

    print()
    typewriter("You breach the fortress gates.")
    fortress_progress = 0

    while fortress_progress < 5:
        print()
        print(f"_____ FORTRESS FIGHT {fortress_progress + 1}/5 _____")

        enemy = random.choice(wasteland_enemies)()
        print(f"A {enemy.name} appears!")
        seen_enemies.add(enemy.name)

        won = combat(enemy)

        if not won:
            print()
            print("You were forced out of the fortress.")
            fortress_progress = 0
            return False

        fortress_progress += 1

    print()
    typewriter("The boss comes forward...")
    print()

    boss = FortressBossEnemy()
    print("_____ FORTRESS BOSS _____")
    print()
    typewriter(f"The {boss.name} steps forward!")
    print()

    seen_enemies.add(boss.name)
    won = combat(boss)

    if won:
        print()
        typewriter("The Scrap Lord has been defeated.")
        fortress_completed = True
        dead_sector_unlocked = True
        player.health = player.max_health
        print(f"HP fully restored: {player.health}/{player.max_health}")
        return True
    else:
        return False



class Player:

    def __init__(self, name, health, attack):

        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack


class Enemy:

    def __init__(
        self,
        name,
        health,
        attack,
        money,
        drop,
        drop_chance,
        rarity
    ):

        self.name = name
        self.health = health
        self.attack = attack
        self.money = money
        self.drop = drop
        self.drop_chance = drop_chance
        self.rarity = rarity


class ThugEnemy(Enemy):

    def __init__(self):

        super().__init__(
            name="Thug",
            health=25,
            attack=random.randint(2, 4),
            money=random.randint(6, 12),
            drop=None,
            drop_chance=0,
            rarity = "common"
        )


class BanditEnemy(Enemy):

    def __init__(self):

        super().__init__(
            name="Bandit",
            health=14,
            attack=random.randint(1, 3),
            money=random.randint(10, 18),
            drop="Wood",
            drop_chance=35,
            rarity = "common"
        )


class OutlawEnemy(Enemy):

    def __init__(self):

        super().__init__(
            name="Outlaw",
            health=50,
            attack=random.randint(2, 10),
            money=random.randint(18, 30),
            drop="Rope",
            drop_chance=35,
            rarity = "uncommon"
        )



class HunterEnemy(Enemy):

    def __init__(self):

        super().__init__(
            name="Hunter",
            health=30,
            attack=random.randint(2, 5),
            money=random.randint(12, 20),
            drop="Leather",
            drop_chance=25,
            rarity = "uncommon"
        )
class RavagerEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name = "Ravager",
            health = 25,
            attack = random.randint(4, 7),
            money=random.randint(20, 25),
            drop=None,
            drop_chance=0,
            rarity = "rare"
    )

class WarlordEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name = "Warlord",
            health = 75,
            attack = random.randint(7,12),
            money=random.randint(50,62),
            drop=None,
            drop_chance=0,
            rarity="epic"
        )


class CampBossEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name="Camp Leader",
            health=250,
            attack=random.randint(10, 21),
            money=random.randint(50, 75),
            drop="Stone",
            drop_chance=100,
            rarity = "???"
        )


# WASTELAND ENEMIES

class RaiderEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name="Raider",
            health=120,
            attack=random.randint(5, 10),
            money=random.randint(25, 40),
            drop="Stone",
            drop_chance=40,
            rarity="common"
        )


class ScavengerEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name="Wasteland Hunter",
            health=150,
            attack=random.randint(6, 12),
            money=random.randint(30, 50),
            drop="Leather",
            drop_chance=40,
            rarity="common"
        )


class BruteEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name="Wasteland Brute",
            health=175,
            attack=random.randint(8, 15),
            money=random.randint(40, 60),
            drop="Stone",
            drop_chance=30,
            rarity="uncommon",
        )

class FortressBossEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name = "Scrap Lord",
            health = 350,
            attack = random.randint(12, 24),
            money = random.randint(80, 110),
            drop ="Iron",
            drop_chance=100,
            rarity="???"
        )

# DEAD SECTOR ENEMIES

class StalkerEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name="Stalker",
            health=270,
            attack=random.randint(15, 22),
            money=random.randint(50, 75),
            drop=None,
            drop_chance=0,
            rarity="common"
        )

class DrifterEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name="Drifter",
            health=250,
            attack=random.randint(19, 25),
            money=random.randint(70, 95),
            drop="Iron",
            drop_chance=25,
            rarity="uncommon"
        )

class RenegadeEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name = "Renegade",
            health = 290,
            attack=random.randint(20, 27),
            money = random.randint(90, 98,),
            drop="Strap",
            drop_chance=35,
            rarity="rare"
        )

class JustToDoSomeKillinEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name = "Warden",
            health = 380,
            attack = random.randint(39, 42),
            money = random.randint(100, 150),
            drop=None,
            drop_chance=0,
            rarity="epic",
        )
    

dead_sector_enemies = [
    StalkerEnemy,
    DrifterEnemy,
    RenegadeEnemy,
]


all_enemies = [
    OutlawEnemy,
    BanditEnemy,
    ThugEnemy,
    HunterEnemy,
    RavagerEnemy,
    WarlordEnemy,
]


wasteland_enemies = [
    RaiderEnemy,
    BruteEnemy,
    ScavengerEnemy
]


player = Player(
    "null",
    100,
    1
)


typewriter(
    "The world isn't what it used to be.",
    speed=0.02
)

typewriter(
    "People don't travel alone anymore.",
    speed=0.02
)

typewriter(
    "The roads aren't safe, and the wilderness is worse.",
    speed=0.02
)

typewriter(
    "You've left everything you knew behind.",
    speed=0.02
)

typewriter(
    "You don't have much.",
    speed=0.02
)

typewriter(
    "A weapon, a few supplies, and a reason to keep moving.",
    speed=0.02
)

typewriter(
    "Where you go from here is up to you.",
    speed=0.02
)

print()

typewriter(
    "_____ COMMANDS _____"
)

print("WASD - moves around")
print("map - displays the map")
print("enemies - shows enemies you've encountered")
print("inventory - shows your inventory")
print("save - saves game")
print("load - loads game")
print("rock speedrun - activates rock speedrun")
print("help - displays this")

print()

animation("Loading", speed = 0.3)

print()

clear_input()

player.name = input(
    "What is your name? "
)


while True:
    moved = False
    if rock_speedrun == True:
        weapon = "Rock"
        

    command = input("> ").strip()

    if command == "map":

        show_map()

    elif command == "w":

        if player_y > 0:

            moved = move_player(
                player_x,
                player_y - 1
            )

            if moved:
                print("You moved forward.")


    elif command == "s":

        if player_y < height - 1:

            moved = move_player(
                player_x,
                player_y + 1
            )

            if moved:
                print("You moved backwards.")


    elif command == "a":

        if player_x > 0:

            moved = move_player(
                player_x - 1,
                player_y
            )

            if moved:
                print("You moved to your left.")


    elif command == "d":

        if player_x < width - 1:

            moved = move_player(
                player_x + 1,
                player_y
            )

            if moved:
                print("You moved to your right.")

    elif command == "help":

        typewriter(
            "_____ COMMANDS _____"
        )

        print("WASD - moves around")
        print("map - displays the map")
        print("enemies - shows enemies you've encountered")
        print("inventory - shows your inventory")
        print("save - saves game")
        print("load - loads game")
        print("rock speedrun - activates rock speedrun")
        print("help - displays this")

        print()

    if moved:
    
            if zone == "Plains":

                if player_x == 1 and player_y == 4:

                    print()
                    typewriter("You arrive at the Shop.")
                    print()

                    shop()

                elif player_x == 3 and player_y == 2:

                    print()
                    typewriter("You arrive at the Workshop.")
                    print()

                    workshop()

            elif zone == "Wastelands":

                if player_x == 5 and player_y == 2:

                    print()
                    typewriter("You arrive at the Wasteland Workshop.")
                    print()

                    workshop()

                elif player_x == 8 and player_y == 1:

                    print()
                    typewriter("You arrive at the Wasteland Shop.")
                    print()

                    shop()

            elif zone == "Dead Sector":

                if player_x == 2 and player_y == 3:
                    print()
                    typewriter("You arrive at the Shop.")
                    print()
                    shop()

                elif player_x == 5 and player_y == 3:
                    print()
                    typewriter("You arrive at the Workshop.")
                    print()
                    workshop()


    if command == "enemies":

        show_enemies()

    elif command == "inventory" or command == "i":

        show_inventory()

    elif command == "save":
        save_game()

    elif command == "load":
        load_game()

    elif command == "rock speedrun":
        rock_speedruns()
