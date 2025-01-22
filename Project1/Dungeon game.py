import sys


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

# now we will try and make the game logic
def game_loop():
    room_desc()
    intro()
    while True:
        action = player_action()
        if action == "quit":
            quit_game()
        else:
            unknown_word()

# I guess this will start the game?
game_loop()