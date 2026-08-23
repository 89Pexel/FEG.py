import sys
import time
import random
import msvcrt
import json
import os

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

seen_enemies = set()

wooden_sword = False
throw_rock_multi = 0

camp_progress = 0
camp_completed = False

new_zone_unlocked = False

zone = "Plains"

def save_game():

    filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "save.json"
    )

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
        "zone": zone
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

    filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "save.json"
    )

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

        print("__________ THE WASTELANDS __________")

    grid[player_y][player_x] = 'P'

    for row in grid:
        print(' '.join(row))


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
            print("You don't have anything else you can craft yet.")

        elif choice == "2":

            typewriter(
                "Already leaving? Alright, come back when you find something worth building.",
                speed=0.02
            )

            break

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

    throw_used = 0
    throw_rock_multi = 0

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

            option = input("> ")
            clear_input()

            if option == "1":

                player.attack = random.randint(3, 7)

                for i in range(3):

                    dots = (i % 3) + 1

                    sys.stdout.write(
                        "\r" + " " * 30 + "\r"
                    )

                    sys.stdout.flush()

                    typewriter1(
                        "Hitting with rock" + "." * dots,
                        speed=0.02
                    )

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

                    typewriter(
                        "Throwing rock...",
                        speed=0.02
                    )

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

                    typewriter(
                        "Throwing rocks...",
                        speed=0.2
                    )

                    time.sleep(2)

                    player.attack = random.randint(7, 12)

                    enemy.health -= player.attack

                    print()
                    print(f"You dealt {player.attack} damage!")
                    print(
                        f"{enemy.name} health: "
                        f"{max(0, enemy.health)}"
                    )

                    throw_rock_multi += 1



            else:

                print("That's not an option.")
                continue

        elif weapon == "Wooden Sword":

            print("[1] Slice")

            if enemies_killed >= 40:

                print("[2] Slash")

            option = input("> ")

            if option == "1":

                typewriter(
                    "Slicing...",
                    speed=0.05
                )

                time.sleep(1)

                player.attack = random.randint(9, 19)

                enemy.health -= player.attack

                print()
                print(f"You dealt {player.attack} damage!")
                print(
                    f"{enemy.name} health: "
                    f"{max(0, enemy.health)}"
                )

            elif option == "2" and enemies_killed >= 40:

                typewriter(
                    "Slashing...",
                    speed=0.7
                )

                time.sleep(1.4)

                player.attack = random.randint(15, 29)

                enemy.health -= player.attack

                print()
                print(f"You dealt {player.attack} damage!")
                print(
                    f"{enemy.name} health: "
                    f"{max(0, enemy.health)}"
                )


            else:

                print("That's not an option.")
                continue

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

    if not wooden_sword:

        typewriter("Beware.")
        typewriter("This area is not for beginners.")

        print()
        print("Recommended:")
        print("- Wooden Sword")
        print("- Lots of kills")
        print("- Plenty of money")
        print("- High maximum HP")

        print()
        print("You don't have a Wooden Sword yet.")
        print("You should probably come back later.")

        return False

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

    choice = input("> ")
    clear_input()

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

        choice = input("> ")
        clear_input()

        if choice == "2":

            break

        elif choice != "1":

            print("That's not an option.")


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

            player_x = 0
            player_y = 2

            explored = [(0, 2)]

            print()
            print(
                "_____ THE WASTELANDS _____"
            )

            typewriter(
                "You leave the plains behind."
            )

            typewriter(
                "Whatever is waiting here is worse."
            )

        # Endless Grounds
        elif (new_x, new_y) == (9, 4):

            player_x = new_x
            player_y = new_y

            infinite_area()

        # Normal unexplored Plains tile
        elif (new_x, new_y) not in explored:

            enemy = random.choice(
                all_enemies
            )()

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

        # Normal unexplored Wastelands tile
        elif (new_x, new_y) not in explored:

            enemy = random.choice(
                wasteland_enemies
            )()

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

def show_enemies():

    print("_____ ENEMIES _____")

    for enemy in all_enemies + wasteland_enemies:

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
        drop_chance
    ):

        self.name = name
        self.health = health
        self.attack = attack
        self.money = money
        self.drop = drop
        self.drop_chance = drop_chance


class ThugEnemy(Enemy):

    def __init__(self):

        super().__init__(
            name="Thug",
            health=25,
            attack=random.randint(2, 4),
            money=random.randint(6, 12),
            drop=None,
            drop_chance=0
        )


class BanditEnemy(Enemy):

    def __init__(self):

        super().__init__(
            name="Bandit",
            health=14,
            attack=random.randint(1, 3),
            money=random.randint(10, 18),
            drop="Wood",
            drop_chance=35
        )


class OutlawEnemy(Enemy):

    def __init__(self):

        super().__init__(
            name="Outlaw",
            health=50,
            attack=random.randint(2, 10),
            money=random.randint(18, 30),
            drop="Rope",
            drop_chance=35
        )


class LeatherEnemy(Enemy):

    def __init__(self):

        super().__init__(
            name="Hunter",
            health=30,
            attack=random.randint(2, 5),
            money=random.randint(12, 20),
            drop="Leather",
            drop_chance=25
        )


class CampBossEnemy(Enemy):

    def __init__(self):

        super().__init__(
            name="Camp Leader",
            health=100,
            attack=random.randint(6, 12),
            money=random.randint(50, 75),
            drop="Stone",
            drop_chance=100
        )


# WASTELAND ENEMIES

class RaiderEnemy(Enemy):

    def __init__(self):

        super().__init__(
            name="Raider",
            health=60,
            attack=random.randint(5, 10),
            money=random.randint(25, 40),
            drop="Stone",
            drop_chance=40
        )


class ScavengerEnemy(Enemy):

    def __init__(self):

        super().__init__(
            name="Wasteland Hunter",
            health=75,
            attack=random.randint(6, 12),
            money=random.randint(30, 50),
            drop="Leather",
            drop_chance=40
        )


class BruteEnemy(Enemy):

    def __init__(self):

        super().__init__(
            name="Wasteland Brute",
            health=110,
            attack=random.randint(8, 15),
            money=random.randint(40, 60),
            drop="Stone",
            drop_chance=30
        )


all_enemies = [
    OutlawEnemy,
    BanditEnemy,
    ThugEnemy,
    LeatherEnemy
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
print("loads - loads game")
print("help - displays this")

print()

player.name = input(
    "What is your name? "
)


while True:
    moved = False

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
        print("help - displays this")

        print()

    if moved and zone == "Plains":

        if player_x == 1 and player_y == 4:

            print()
            typewriter("You arrive at the Shop.")
            print()

            shop()

        if player_x == 3 and player_y == 2:

            print()
            typewriter("You arrive at the Workshop.")
            print()

            workshop()

    if zone == "Wastelands" and player_x == 5 and player_y == 2:

        print()
        typewriter("You arrive at the Wasteland Workshop.")
        print()

        workshop()

    elif zone == "Wastelands" and player_x == 8 and player_y == 1:

        print()
        typewriter("You arrive at the Wasteland Shop.")
        print()

        shop()

    if command == "enemies":

        show_enemies()

    elif command == "inventory" or command == "i":

        show_inventory()

    elif command == "save":
        save_game()

    elif command == "load":
        load_game()
