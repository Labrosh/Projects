import sys

player_location = "starting room"
rooms = {
    "starting room": {
        "description": "You find yourself inside a blank square room. There is an exit to the north, south, east, and west.",
        "exits": {
            "north": "north room",
            "south": "south room",
            "east": "east room",
            "west": "west room"
        }
    },
    "north room": {
        "description": "You are in a room with stone walls. There is an exit to the south.",
        "exits": {
            "south": "starting room"
        }
    },
    "south room": {
        "description": "You are in a damp, dark room. There is an exit to the north.",
        "exits": {
            "north": "starting room"
        }
    },
    "east room": {
        "description": "You are in a brightly lit room. There is an exit to the west.",
        "exits": {
            "west": "starting room"
        }
    },
    "west room": {
        "description": "You are in a room filled with ancient artifacts. There is an exit to the east.",
        "exits": {
            "east": "starting room"
        }
    }
}

def room_desc():
    global player_location
    room = rooms[player_location]
    print(room["description"])

def intro():
    print("Welcome to the dungeon.\n")
    print("You should start by looking around, or maybe checking your inventory.\n")

def player_action():
    player_action = input("What do you want to do? ").strip().lower()
    return player_action

def quit_game():
    print("Goodbye, brave adventurer!")
    sys.exit()

def unknown_word():
    print("I don't understand that word.")

def move(direction):
    global player_location
    current_room = rooms[player_location]
    if direction in current_room["exits"]:
        player_location = current_room["exits"][direction]
        print(f"You move {direction}.")
    else:
        print("You can't go that way.")

def move_north():
    move("north")

def move_south():
    move("south")

def move_east():
    move("east")

def move_west():
    move("west")

def inventory():
    print("You have nothing in your inventory.")

def debug():
    print(player_location)

# lets make a commands dictionary - hopefully this works
commands = {
    "quit": quit_game,
    "exit": quit_game,
    "look": room_desc,
    "inventory": inventory,
    "north": move_north,
    "south": move_south,
    "east": move_east,
    "west": move_west,
    "debug": debug
}


# I think I want to keep game loop near the bottom so I can find it easier
def game_loop():
    room_desc()
    intro()
    while True:
        action = player_action()
        if action in commands:
            command = commands[action]
            if callable(command):
                command()
            else:
                print(command)
        else:
            unknown_word()


# I guess this will start the game?
game_loop()