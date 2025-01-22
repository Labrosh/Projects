import sys

player_location = "starting room"

def room_desc():
    room_desc = "You find yourself inside a blank square room. There is an exit to the north." # this will be the starting room description, but I want to work on making this change base on what is in the room
    print(room_desc)

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

def move_north():
    print("You move north.")
    player_location = "north room"
def move_south():
    print("You move south.")
    player_location = "south room"
def move_east():
    print("You move east.")
    player_location = "east room"
def move_west():
    print("You move west.")
    player_location = "west room"
def inventory():
    print("You have nothing in your inventory.")


# lets make a commands dictionary - hopefully this works
commands = {
    "quit": quit_game,
    "exit": quit_game,
    "look": room_desc,
    "inventory": inventory,
    "north": move_north,
    "south": move_south,
    "east": move_east,
    "west": move_west
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