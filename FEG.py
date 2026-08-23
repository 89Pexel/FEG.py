import sys
import time
import random

player_x = 0
player_y = 4

old_x = player_x
old_y = player_y

width = 10
height = 5

enemies_killed = 0
deaths = 0

moved = False

weapon = "Rock"

explored = [(0, 4)]

inventory = {}

money = 50

health_upgrades = 0
restores = 0

seen_enemies = set()

wooden_sword = False


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

    grid[2][3] = 'W'
    grid[4][1] = 'S'

    grid[player_y][player_x] = 'P'

    print("____________ THE PLAINS ____________")

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
                    print(
                        f"You need 3 Wood and 1 Leather."
                    )

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
            print("Sell what? I haven't even set that up yet.")

        elif choice == "3":

            while True:
                print()
                print("_____ HEALTH _____")
                print(f"HP: {player.health}/{player.max_health}")
                print()

                print("[1] Heal 10 HP - $8")
                print("[2] Heal 50 HP - $30")

                restore_price = 50 + (restores * 15)

                print(
                    f"[3] Restore Full Health - ${restore_price}"
                )

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
                        print(
                            f"HP: {player.health}/{player.max_health}"
                        )
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
                        print(
                            f"HP: {player.health}/{player.max_health}"
                        )
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
                        print(
                            f"HP: {player.health}/{player.max_health}"
                        )
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

    while player.health > 0 and enemy.health > 0:

        print()
        print(f"HP: {player.health}")
        print(f"Enemy HP: {enemy.health}")
        print()

        # ---------------- ROCK ----------------

        if weapon == "Rock":

            print("[1] Hit with rock")

            if enemies_killed >= 5:
                print("[2] Throw Rock")

            option = input("> ")

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
                print(
                    f"You dealt {player.attack} damage!"
                )
                print(
                    f"{enemy.name} health: "
                    f"{max(0, enemy.health)}"
                )

            elif option == "2" and enemies_killed >= 5:

                typewriter(
                    "Throwing rock...",
                    speed=0.02
                )

                player.attack = random.randint(4, 8)

                enemy.health -= player.attack

                print()
                print(
                    f"You dealt {player.attack} damage!"
                )
                print(
                    f"{enemy.name} health: "
                    f"{max(0, enemy.health)}"
                )

            else:
                print("That's not an option.")
                continue

        # ---------------- WOODEN SWORD ----------------

        elif weapon == "Wooden Sword":

            print("[1] Slice")

            option = input("> ")

            if option == "1":

                typewriter(
                    "Slicing...",
                    speed=0.05
                )

                time.sleep(1)

                player.attack = random.randint(5, 19)

                enemy.health -= player.attack

                print()
                print(
                    f"You dealt {player.attack} damage!"
                )
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

        # ---------------- ENEMY DEFEATED ----------------

        if enemy.health <= 0:

            enemies_killed += 1

            print()

            money += enemy.money

            typewriter(
                f"You defeated the {enemy.name}!"
            )

            print(
                f"Enemies killed: {enemies_killed}"
            )

            print(
                f"You found ${enemy.money}!"
            )

            print(f"Money: ${money}")

            # Drop chance

            if (
                enemy.drop is not None
                and random.randint(1, 100)
                <= enemy.drop_chance
            ):

                inventory[enemy.drop] = (
                    inventory.get(enemy.drop, 0) + 1
                )

                print(
                    f"They dropped: {enemy.drop}!"
                )

            return True

        # ---------------- ENEMY ATTACK ----------------

        enemy_damage = enemy.attack

        player.health -= enemy_damage

        print()
        print(
            f"The {enemy.name} attacks!"
        )

        print(
            f"You take {enemy_damage} damage."
        )

        # ---------------- PLAYER DEATH ----------------

        if player.health <= 0:

            deaths += 1

            print()

            typewriter(
                "You were defeated."
            )

            print(
                f"Deaths: {deaths}"
            )

            player.max_health = max(
                10,
                player.max_health - 10
            )

            player.health = player.max_health

            print(
                f"Your new maximum health is "
                f"{player.max_health}."
            )

            print(
                "You remain in this area."
            )

            return False


def move_player(new_x, new_y):
    global player_x, player_y

    old_x = player_x
    old_y = player_y

    if (new_x, new_y) not in explored:

        enemy = random.choice(all_enemies)()

        print(
            f"A {enemy.name} appears!"
        )

        seen_enemies.add(enemy.name)

        won = combat(enemy)

        if won:
            player_x = new_x
            player_y = new_y

            explored.append(
                (new_x, new_y)
            )

        else:
            player_x = old_x
            player_y = old_y

    else:
        player_x = new_x
        player_y = new_y


def show_enemies():
    print("_____ ENEMIES _____")

    for enemy in all_enemies:

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


# __________________________________


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
            drop_chance=15
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
            drop_chance=50
        )


all_enemies = [
    OutlawEnemy,
    BanditEnemy,
    ThugEnemy,
    LeatherEnemy
]


player = Player(
    "null",
    100,
    1
)


# INTRO

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
print("help - displays this")

print()

player.name = input(
    "What is your name? "
)


# MAIN LOOP

while True:

    command = input("> ").strip()

    if command == "map":

        show_map()

    elif command == "w":

        if player_y > 0:
            move_player(
                player_x,
                player_y - 1
            )
            moved = True

    elif command == "s":

        if player_y < height - 1:
            move_player(
                player_x,
                player_y + 1
            )
            moved = True

    elif command == "a":

        if player_x > 0:
            move_player(
                player_x - 1,
                player_y
            )
            moved = True

    elif command == "d":

        if player_x < width - 1:
            move_player(
                player_x + 1,
                player_y
            )
            moved = True

    elif command == "help":

        typewriter(
            "_____ COMMANDS _____"
        )

        print("WASD - moves around")
        print("map - displays the map")
        print("enemies - shows enemies you've encountered")
        print("inventory - shows inventory")
        print("help - displays this")

        print()

    if moved and player_x == 1 and player_y == 4:
        shop()

    if moved and player_x == 3 and player_y == 2:
        workshop()

    if command == "enemies":

        print(
            "RIP LOL KK BRUH FR NP YW WP ROFL"
        )

        show_enemies()

    elif command == "inventory" or command == "i":

        show_inventory()

    moved = False
