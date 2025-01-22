import sys

# A simple room description for now
room_desc = "You find yourself inside a blank square room. There is an exit to the north."

print("Welcome to the dungeon.\n")
print("You should start by looking around, or maybe checking your inventory.\n")

while True:
    player_action = input("What do you want to do? ").strip().lower()
    
    if player_action == "quit":
        print("Goodbye, brave adventurer!")
        sys.exit()
    elif player_action == "look":
        print(room_desc)
    else:
        print("I don't understand that word.")
