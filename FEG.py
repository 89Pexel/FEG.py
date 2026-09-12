import sys
import time
import random
import json
import os

'''
I use AI for the prompts cause AI sounds cool, anything else, not really.
'''

try:
    import msvcrt
    HAS_MS = True
except ImportError:
    HAS_MS = False

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
stone_sword = False

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
speed_upgrades = 0
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

energy_drink = False

current_weather = "Clear"
weather_speed_penalty = 0

now_time = 7

now_current = "Morning"

now_current_random_morning = ["It's a new day.", "The sun rises over the horizon.", "A new day begins."]
now_current_random_night = ["The sun sets, and darkness falls.", "Night descends upon the land.", "The stars twinkle in the night sky."]

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


def set_weather(new_weather, force=False):

    global current_weather, weather_speed_penalty

    if new_weather == current_weather and not force:
        return

    player.speed += weather_speed_penalty
    weather_speed_penalty = 0
    current_weather = new_weather

    print()
    print(f"_____ WEATHER: {current_weather.upper()} _____")

    if current_weather == "Clear":
        if zone == "Plains":
            print("The sky clears above the Plains. Your speed returns to normal.")
        elif zone == "Wastelands":
            print("The Wasteland sky is clear again. Travel is easier for now.")
        else:
            print("The Dead Sector is still. The damaged machinery falls silent.")

    elif current_weather == "Cloudy":
        if zone == "Plains":
            print("Dark clouds gather over the Plains, but travel is still normal.")
        elif zone == "Wastelands":
            print("Clouds drift over the Wastelands. The heat eases for a while.")
        else:
            print("Low clouds hang over the Dead Sector.")

    elif current_weather == "Rain":
        if zone == "Plains":
            weather_speed_penalty = 1
            print("You hear rain across the Plains. Your speed is reduced by 1.")
        elif zone == "Wastelands":
            weather_speed_penalty = random.randint(1, 2)
            print("Rain is rare in the Wastelands. Floodwater slows your movement.")
            print(f"Your speed is reduced by {weather_speed_penalty}.")
        else:
            print("You hear rain hissing against dead metal. Nothing changes here.")

    elif current_weather == "Thunderstorm":
        if zone == "Plains":
            weather_speed_penalty = 1
            print("Thunder rolls across the Plains. Your speed is reduced by 1.")
        elif zone == "Wastelands":
            weather_speed_penalty = 2
            print("A violent storm floods the Wastelands. Your speed is reduced by 2.")
        else:
            print("Lightning tears through the Dead Sector's ruined machinery.")
            print("Storm strikes will damage enemies at the start of battle.")

    player.speed -= weather_speed_penalty
    print(f"Current speed: {player.speed}")
    print()


def update_weather():

    if random.randint(1, 100) > 25:
        return

    weather_options = {
        "Plains": ["Clear"] * 50 + ["Cloudy"] * 25 + ["Rain"] * 18 + ["Thunderstorm"] * 7,
        "Wastelands": ["Clear"] * 60 + ["Cloudy"] * 28 + ["Rain"] * 6 + ["Thunderstorm"] * 6,
        "Dead Sector": ["Clear"] * 50 + ["Cloudy"] * 20 + ["Rain"] * 15 + ["Thunderstorm"] * 15,
    }

    set_weather(random.choice(weather_options[zone]))


def nowtime():
    global now_current
    global now_time
    if now_time == 24:
        now_time = 0
        now_current = "Day"
        print(random.choice(now_current_random_morning))
    elif now_time == 12:
        now_current = "Night"
        print(random.choice(now_current_random_night))





def bot():
    print()
    print("_____ SCRAP GUIDE BOT _____")
    print("I can explain the world, your stats, and what to do next.")
    print("Type 'help' to see everything I know, or 'exit' to leave.")

    while True:

        command = input("BOT > ").strip().lower()

        if command in ("exit", "quit", "leave", "back"):
            print("Guide Bot offline. Stay alive out there.")
            print()
            break

        elif command in ("", "..."):
            print("Ask me something, or type 'help'.")

        elif command in ("help", "commands", "what can you do"):
            print()
            print("_____ GUIDE BOT COMMANDS _____")
            print("status     - view your current stats")
            print("goal       - learn what to do next")
            print("combat     - explain your weapon moves")
            print("speed      - explain the speed system")
            print("shop       - view upgrade prices")
            print("inventory  - view your items")
            print("enemies    - view enemies you have seen")
            print("zones      - learn about each area")
            print("map        - display the map")
            print("tips       - get survival advice")
            print("weather    - learn about the weather system")
            print("meaning of life - asks the bot a question about life")
            print("exit       - return to the game")
            print()

        elif command in ("status", "stats", "me", "player"):
            print()
            print("_____ PLAYER STATUS _____")
            print(f"Name: {player.name}")
            print(f"Zone: {zone}")
            print(f"Position: {player_x}, {player_y}")
            print(f"HP: {player.health}/{player.max_health}")
            print(f"Weapon: {weapon}")
            print(f"Speed: {player.speed}")
            print(f"Money: ${money}")
            print(f"Enemies defeated: {enemies_killed}")
            print(f"Deaths: {deaths}")
            if energy_drink:
                print("Energy Drink: Active for your next battle")
            else:
                print("Energy Drink: Not active")
            print()

        elif command in ("goal", "goals", "objective", "objectives", "what now", "next"):
            print()
            print("_____ CURRENT OBJECTIVE _____")

            if zone == "Plains":
                if not camp_completed:
                    print("Defeat the Enemy Camp at the east side of the Plains.")
                    print("It takes five fights followed by the Camp Leader.")
                    print("Clearing it opens the path to the Wastelands.")
                elif not new_zone_unlocked:
                    print("The Enemy Camp is cleared, but the path is still closed.")
                else:
                    print("The Wastelands entrance is open at the east side of the Plains.")

            elif zone == "Wastelands":
                if not fortress_completed:
                    print("Defeat the Scrap Fortress at position 3, 3.")
                    print("It has five fights followed by the Scrap Lord.")
                    print("Clearing it opens the Dead Sector.")
                else:
                    print("The Dead Sector entrance is open to the east.")

            elif zone == "Dead Sector":
                print("Explore the Dead Sector, earn resources, and prepare for tougher foes.")
                print("Your speed upgrades and Energy Drinks matter most here.")

            print()

        elif command in ("combat", "fight", "attacks", "moves", "weapon"):
            print()
            print("_____ COMBAT GUIDE _____")
            print(f"Current weapon: {weapon}")

            if weapon == "Rock":
                print("Hit with Rock is always available.")
                print("More Rock moves unlock at 5, 10, 50, 100, 125, 210, 250 kills.")
            elif weapon == "Wooden Sword":
                print("Slice is always available.")
                print("Slash unlocks at 40 kills and Thrust unlocks at 75 kills.")
            elif weapon == "Stone Sword":
                print("Swipe is always available.")
                print("Crash unlocks at 65 kills, Shatter at 150, and Annihilate at 200.")
            elif weapon == "Iron Sword":
                print("Smash is always available.")
                print("Mash unlocks at 200 kills, Lash at 350, and Bash at 400.")

            print("Tip: stronger moves often have a per-battle limit, so save them for hard fights.")
            print()

        elif command in ("speed", "fast", "double attack", "extra attack"):
            print()
            print("_____ SPEED GUIDE _____")
            print(f"Your current speed: {player.speed}")
            print("If an enemy is faster, it may attack a second time.")
            print("Speed difference: 1 / 2 / 3 / 4 / 5 / 6 / 7+")
            print("Extra-hit chance: 5% / 25% / 35% / 55% / 60% / 80% / 100%")
            print("If you are faster, you may strike again: 3% / 6% / 10% / 15% / 20% / 25%.")
            print("Buy Speed upgrades at shops, or use an Energy Drink for +2 speed in one battle.")
            print("You can use Energy Drinks by saying 'energy drink' before a fight.")
            print()

        elif command in ("shop", "upgrades", "upgrade", "prices"):
            health_price = 25 + (health_upgrades * 15)
            speed_price = 30 * (2 ** speed_upgrades)

            print()
            print("_____ SHOP GUIDE _____")
            print(f"Next Health upgrade: ${health_price} for +10 max HP")
            print(f"Next Speed upgrade: ${speed_price} for +1 speed")
            print("Speed prices double after every purchase, so choose upgrades carefully.")
            print("Health services can also restore HP during a difficult run.")
            print()

        elif command in ("inventory", "items", "bag"):
            print()
            print("_____ INVENTORY _____")
            if inventory:
                for item, amount in inventory.items():
                    print(f"{item} x{amount}")
            else:
                print("Your inventory is empty.")
            print()

        elif command in ("enemies", "enemy", "seen enemies"):
            show_enemies()

        elif command in ("zones", "zone", "areas", "area", "places"):
            print()
            print("_____ ZONE GUIDE _____")
            print("Plains: your starting area, with the Shop, Workshop, and Enemy Camp.")
            print("Wastelands: stronger enemies, a Scrap Fortress, and more valuable drops.")
            print("Dead Sector: extremely fast enemies, high rewards, and dangerous encounters.")
            print("Endless Grounds: fight repeatedly when you want more kills and drops.")
            print()

        elif command in ("map", "show map"):
            show_map()

        elif command in ("tips", "tip", "advice", "help me"):
            print()
            print("_____ SURVIVAL TIPS _____")
            print("- Save before entering the Enemy Camp or Scrap Fortress.")
            print("- Sell spare drops for money, but keep crafting materials for swords.")
            print("- Buy health before a boss if your maximum HP is low.")
            print("- If an enemy is much faster, use an Energy Drink or buy Speed upgrades.")
            print("- Explore cleared tiles safely when you need to reach a shop.")
            print()

        elif command in ("hello", "hi", "hey"):
            print(f"Hello, {player.name}. Type 'help' if you need guidance.")

        elif command in ("meaning of life", "life", "question"):
            print("The meaning of life is a question that has being asked for a long time.")
            print("Some say it's to find happiness, others say it's to find purpose.")
            print("The real reason cannot simply be stated.")
            print("You can find the meaning of life using the A0Z25 cipher.")
            print("E, C.")
            print("If you don't get this. Say whats going on.")

        elif command in ("whats going on", "what's going on", "what is going on"):
            print("42")
            print("That's the meaning of life according to Douglas Adams.")
            print("Have you read The Hitchhiker's Guide to the Galaxy?")
            print("If you haven't, that's why you don't understand it.")

        elif command in ("weather", "weather system"):
            print()
            print("_____ WEATHER GUIDE _____")
            print("Weather can change randomly as you explore.")
            print("Clear: normal speed, no effects.")
            print("Cloudy: normal speed, no effects.")
            print("Rain: reduces speed by 1-2 in the Wastelands, 1 in the Plains.")
            print("Thunderstorm: reduces speed by 2 in the Wastelands, 1 in the Plains.")
            print("In the Dead Sector, weather has no effect on your speed.")
            print(f"Current weather: {current_weather}")
            print()

        else:
            print("I do not understand that yet. Type 'help' for available commands.")
        
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
        "speed_upgrades": speed_upgrades,
        "speed": player.speed,
        "restores": restores,
        "explored": explored,
        "seen_enemies": list(seen_enemies),
        "wooden_sword": wooden_sword,
        "camp_completed": camp_completed,
        "new_zone_unlocked": new_zone_unlocked,
        "zone": zone,
        "fortress_completed": fortress_completed,
        "dead_sector_unlocked": dead_sector_unlocked,
        "stone_sword": stone_sword,
        "energy_drink": energy_drink,

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
    global health_upgrades, speed_upgrades, restores
    global explored, seen_enemies
    global wooden_sword
    global camp_completed, new_zone_unlocked
    global zone
    global fortress_completed
    global dead_sector_unlocked
    global stone_sword
    global energy_drink

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
        speed_upgrades = data.get("speed_upgrades", 0)
        player.speed = data.get("speed", 5)
        restores = data["restores"]

        explored = [tuple(pos) for pos in data["explored"]]
        seen_enemies = set(data["seen_enemies"])

        wooden_sword = data["wooden_sword"]

        camp_completed = data["camp_completed"]
        new_zone_unlocked = data["new_zone_unlocked"]

        zone = data["zone"]

        fortress_completed = data["fortress_completed"]

        dead_sector_unlocked = data["dead_sector_unlocked"]
        stone_sword = data["stone_sword"]
        energy_drink = data.get("energy_drink", False)

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
    if HAS_MS:
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

    global wooden_sword, weapon, stone_sword

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

        elif choice == "1" and wooden_sword and stone_sword == False:

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
                    stone_sword = True

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

    global money, health_upgrades, speed_upgrades, restores

    while True:

        print("_____ SHOP _____")

        typewriter(
            "Oh great. You again, what d'ya need?",
            speed=0.02
        )

        print()
        print(f"Money: ${money}")
        print(f"HP: {player.health}/{player.max_health}")
        print(f"Speed: {player.speed}")
        print()

        print("[1] Buy Health")
        print("[2] Buy Speed")
        print("[3] Sell Drops")
        print("[4] Health")
        print("[5] Leave")

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

            speed_price = 30 * (2 ** speed_upgrades)

            print()
            print("Speed upgrade: +1 speed")
            print(f"Cost: ${speed_price}")

            if money >= speed_price:

                money -= speed_price
                speed_upgrades += 1
                player.speed += 1

                print("You feel lighter on your feet.")
                print(f"Speed: {player.speed}")
                print(f"Money: ${money}")

            else:

                print("You can't afford that.")

        elif choice == "3":

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

        elif choice == "4":

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

        elif choice == "5":

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
    global energy_drink

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
        print(f"HP: {player.health} | Speed: {player.speed}")
        print(f"Enemy HP: {enemy.health} | Enemy speed: {enemy.speed}")
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
                            print("[5] Throw multiple boulders")
                            if enemies_killed >= 125:
                                print("[6] Throw Mountain")
                                if enemies_killed >= 210:
                                    print("[7] Throw a Mountain Range")
                                    if enemies_killed >= 250:
                                        print("[8] Throw a Meteor")

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

            elif option == "7" and enemies_killed >= 210:
                player.attack = random.randint(45, 59)

                animation("Throwing mountain range")

                enemy.health -= player.attack
                print()
                print(f"You dealt {player.attack} damage!")
                print(
                    f"{enemy.name} health: "
                    f"{max(0, enemy.health)}"
                )

            elif option == "8" and enemies_killed >= 250:
                player.attack = random.randint(55, 70)

                animation("Throwing meteor")

                enemy.health -= player.attack
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
                if enemies_killed >= 350:
                    print("[3] Lash")
                    if enemies_killed >= 400:
                        print("[4] Bash")
                

            choice = input("> ")

            if choice == "1":
                animation("Smashing")
                player.attack = random.randint(62, 68)
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
                    player.attack = random.randint(67, 75)
                    enemy.health -= player.attack
                    mash_times += 1
                    print()
                    print(f"You dealt {player.attack} damage!")
                    print(
                        f"{enemy.name} health: "
                        f"{max(0, enemy.health)}"
                    )

            elif choice == "3" and enemies_killed >= 350:
                if lash_times == 3:
                    print("Lashing too much times will get you mashed and lashed.")
                    continue
                else:
                    animation("Lashing")
                    player.attack = random.randint(82, 92)
                    enemy.health -= player.attack
                    lash_times += 1
                    print()
                    print(f"You dealt {player.attack} damage!")
                    print(
                        f"{enemy.name} health: "
                        f"{max(0, enemy.health)}"
                    )

            elif choice == "4" and enemies_killed >= 400:
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

        

        player_speed_difference = player.speed - enemy.speed
        player_extra_attack_chances = {
            1: 3,
            2: 6,
            3: 10,
            4: 15,
            5: 20,
            6: 25,
        }
        player_extra_attack_chance = player_extra_attack_chances.get(
            min(player_speed_difference, 6),
            0
        )

        if (
            enemy.health > 0
            and player_extra_attack_chance > 0
            and random.randint(1, 100) <= player_extra_attack_chance
        ):

            print("You are faster and strike again!")

            enemy.health -= player.attack

            print(f"You dealt another {player.attack} damage!")
            print(f"{enemy.name} health: {max(0, enemy.health)}")

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

            if energy_drink:
                player.speed -= 2
                energy_drink = False
                print("The Energy Drink wears off.")

            return True

        enemy_damage = enemy.attack

        player.health -= enemy_damage

        print()
        print(f"The {enemy.name} attacks!")
        print(f"You take {enemy_damage} damage.")

        speed_difference = enemy.speed - player.speed
        extra_attack_chances = {
            1: 5,
            2: 25,
            3: 35,
            4: 55,
            5: 60,
            6: 80,
            7: 100,
        }
        extra_attack_chance = extra_attack_chances.get(
            min(speed_difference, 7),
            0
        )

        if (
            player.health > 0
            and extra_attack_chance > 0
            and random.randint(1, 100) <= extra_attack_chance
        ):

            print(
                f"The {enemy.name} is faster and attacks again!"
            )

            player.health -= enemy_damage

            print(f"You take another {enemy_damage} damage.")

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

            if energy_drink:
                player.speed -= 2
                energy_drink = False
                print("The Energy Drink wears off.")

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

        enemy = random.choice(plains_enemies)()

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

        enemy = random.choice(plains_enemies)()

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

            enemy = choose_enemy(plains_enemies)

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

    for enemy in plains_enemies + wasteland_enemies + dead_sector_enemies:

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

    def __init__(self, name, health, attack, speed):

        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.speed = speed


class Enemy:

    def __init__(
        self,
        name, health, attack, money, drop, drop_chance, rarity, speed
    ):

        self.name = name
        self.health = health
        self.attack = attack
        self.money = money
        self.drop = drop
        self.drop_chance = drop_chance
        self.rarity = rarity
        self.speed = speed


class ThugEnemy(Enemy):

    def __init__(self):

        super().__init__(
            name="Thug",
            health=25,
            attack=random.randint(2, 4),
            money=random.randint(6, 12),
            drop=None,
            drop_chance=0,
            rarity = "common",
            speed = random.randint(1, 6)
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
            rarity = "common",
            speed = random.randint(4, 6)
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
            rarity = "uncommon",
            speed = random.randint(4, 8)
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
            rarity = "uncommon",
            speed = random.randint(6, 8)
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
            rarity = "rare",
            speed = random.randint(6, 9)
    )

class Poacher(Enemy):
    def __init__(self):
        super().__init__(
            name = "Poacher",
            health = 50,
            attack = random.randint(5, 10),
            money=random.randint(30, 40),
            drop="Leather",
            drop_chance=50,
            rarity = "rare",
            speed = random.randint(7, 9)
    )

class WarlordEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name = "Warlord",
            health = 75,
            attack = random.randint(7,12),
            money=random.randint(50,62),
            drop="Energy Drink",
            drop_chance=25,
            rarity="epic",
            speed = 9
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
            rarity = "???",
            speed = 10
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
            rarity="common",
            speed=random.randint(8, 9)
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
            rarity="common",
            speed=random.randint(7, 9)
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
            speed=random.randint(8, 10)
        )

class HoundEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name="Wasteland Hound",
            health=200,
            attack=random.randint(10, 18),
            money=random.randint(50, 70),
            drop="Leather",
            drop_chance=30,
            rarity="uncommon",
            speed=random.randint(8, 9)
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
            rarity="???",
            speed=12
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
            rarity="common",
            speed=random.randint(12, 15)
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
            rarity="uncommon",
            speed=random.randint(14, 15)
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
            rarity="rare",
            speed=random.randint(15, 17)
        )

class DefectorEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name = "Defector",
            health = 300,
            attack=random.randint(25, 30),
            money = random.randint(100, 120),
            drop="Energy Drink",
            drop_chance=50,
            rarity="rare",
            speed=random.randint(14, 16)
        )

class EngineerEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name = "Engineer",
            health = 320,
            attack=random.randint(30, 35),
            money = random.randint(120, 140),
            drop="Iron",
            drop_chance=50,
            rarity="epic",
            speed=random.randint(10, 12)
        )


class JustToDoSomeKillinEnemy(Enemy):
    def __init__(self):
        super().__init__(
            name = "Warden",
            health = 380,
            attack = random.randint(39, 42),
            money = random.randint(100, 150),
            drop="Energy Drink",
            drop_chance=50,
            rarity="epic",
            speed=random.randint(14, 17)
        )
    

dead_sector_enemies = [
    JustToDoSomeKillinEnemy,
    StalkerEnemy,
    DrifterEnemy,
    RenegadeEnemy,
    DefectorEnemy,
    EngineerEnemy,
]


plains_enemies = [
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
    ScavengerEnemy,
    Poacher,
    HoundEnemy,
]


player = Player(
    "null",
    100,
    1,
    5
)


typewriter("You look around.")
time.sleep(0.2)
typewriter("Empty land. No people. No supplies.")
time.sleep(0.2)
typewriter("You check your inventory.")
time.sleep(1.5)
print()
typewriter("One rock.")
time.sleep(1.5)
print()

typewriter("This is going to be a long day.")

time.sleep(2)

print()

typewriter(
    "_____ COMMANDS _____",
)

print("WASD - moves around")
print("map - displays the map")
print("enemies - shows enemies you've encountered")
print("inventory - shows your inventory")
print("save - saves game")
print("load - loads game")
print("rock speedrun - activates rock speedrun")
print("bot - opens the Scrap Guide Bot")
print("help - displays this")

print()

animation("Loading", speed = 0.3)

print()

print("If you do Ctrl C it will break the game.")

clear_input()

player.name = input(
    "What is your name? "
)


while True:
    moved = False

    now_time += 1
    print(f"Time: {now_time}:00")
    nowtime()
    
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
        print("bot - opens the Scrap Guide Bot")
        print("help - displays this")

        print()

    if command == "Energy Drink" or command == "energy drink" or command == "drink" or command == "Drink":

        if inventory.get("Energy Drink", 0) > 0:

            if energy_drink:

                print()
                print("You already have an Energy Drink active.")

            else:

                inventory["Energy Drink"] -= 1
                energy_drink = True
                player.speed += 2

                print()
                print("You drank an Energy Drink.")
                print("Speed increased by 2 for your next battle.")
                print(f"Speed: {player.speed}")

        else:

            print()
            print(
                "You don't have any Energy Drinks."
            )

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

    elif command == "bot":
        bot()
