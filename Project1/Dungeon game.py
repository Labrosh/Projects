import sys
import random

# Let's try Object Oriented Programming...

# First let's make a class for the player
class Player:
    def __init__(self):
        self.location = "starting room"
        self.inventory = []

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def show_inventory(self):
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("You have the following items:")
            for item in self.inventory:
                print(f"- {item}")

player = Player()


# Next I am going to try and make a class for rooms

class Room:
    def __init__(self, description, items=None, exits=None, key=None):
        self.description = description  # Fixed typo here
        self.items = items if items else []
        self.exits = exits if exits else {}
        self.key = key

    def describe(self):
        print("\n" + "="*40)
        print(self.description)
        if self.items:
            print(f"\nYou see the following items: {', '.join(self.items)}")
        print("="*40 + "\n")

    def is_locked(self, player_inventory):
        return self.key and self.key not in player_inventory

# I think I need to add a dictonary for items, and a function to give a descrption of the item if examanined or picked up
items = {
    "slimy key": {
        "description": "A slimy key that smells of old fish. You found this in the south room."
    },
    "stone key": {
        "description": "A heavy key made of stone. You found this in the north room."
    },
    "shiny key": {
        "description": "A shiny key that sparkles in the light. You found this in the east room."
    },
    "ancient key": {
        "description": "An ancient key that looks like it's been around for centuries. You found this in the west room. It seems to be bigger than the other keys you've found."
    }
}

# I'm going to add a dictionary for the rooms, and then add a function to print the room description
rooms = {
    "starting room": Room(
        description="You find yourself inside a blank square room. There is an exit to the north, south, east, and west.",
        exits={"north": "north room", "south": "south room", "east": "east room", "west": "west room"},
        items=[]
    ),
    "north room": Room(
        description="You are in a room with stone walls. There is an exit to the south. You see a stone key on the ground.",
        exits={"south": "starting room"},
        items=["stone key"]
    ),
    "south room": Room(
        description="You are in a damp, dark room. There is an exit to the north. You see a slimy key on the ground.",
        exits={"north": "starting room"},
        items=["slimy key"],
        key="stone key"
    ),
    "east room": Room(
        description="You are in a brightly lit room. There is an exit to the west. You see a shiny key on the ground.",
        exits={"west": "starting room"},
        items=["shiny key"],
        key="slimy key"
    ),
    "west room": Room(
        description="You are in a room filled with ancient artifacts. There is an exit to the east, and to the west. You see an ancient key on the ground.",
        exits={"east": "starting room", "west": "dungeon exit"},
        items=["ancient key"],
        key="shiny key"
    ),
    "dungeon exit": Room(
        description="You have found the exit to the dungeon. Congratulations!",
        exits={"east": "west room"},
        items=[],
        key="ancient key"
    )
}

# this now prints the room description, and is helpful when moving between rooms
def room_desc():
    room = rooms[player.location]
    print("\n" + "="*40)
    print(f"Location: {player.location.upper()}")
    print("-"*40)
    room.describe()
    print("="*40 + "\n")




recent_prompts = []
# I'm going to add a prompt function to give the player a prompt when they need to make a decision - randomized for variety
def get_prompt():
    prompts = [
        "What do you want to do? ",
        "What's next? ",
        "What's your next move? ",
        "What's the plan? ",
        "What's the next step? ",
        "The darkness is closing in. What now? ",
        "The walls are closing in. What do you do? ",
        "The shadows are moving. What's your move? ",
        "The silence is deafening. What's next? ",
        "The air is thick with anticipation. What's your next move? ",
        "You feel a chill run down your spine. What do you do? ",
        "You hear a faint whisper. What's your next move? ",
        "You feel a presence watching you. What's your next move? ",
        "You feel a sense of dread. What do you do? ",
        "You feel a sense of foreboding. What's your next move? ",
        "You feel a sense of unease. What do you do? ",
        "Something smells foul. What's your next move? ",
        "You hear a faint rustling. What's your next move? ",
        "You hear a faint creaking. What do you do? ",
        "Nice one, adventurer, but what's next? ",
        "ah...this again. What's your next move? ",
        "couldn't think of anything better? What's your next move? ",
        "bored yet? What's your next move? ",
        "I'm getting tired of this. What's your next move? ",
        "I could have guessed that. What's your next move? ",
        "I'm not impressed. What's your next move? ",
        "I'm not amused. What's your next move? ",
        "*Yawn* What's your next move? ",
        "You're not very creative. What's your next move? ",
    ]
    available_prompts = [p for p in prompts if p not in recent_prompts]

    if not available_prompts:
        recent_prompts.clear()
        available_prompts = prompts
    
    chosen_prompt = random.choice(available_prompts)

    recent_prompts.append(chosen_prompt)
    if len(recent_prompts) > 5:
        recent_prompts.pop(0)
    
    return chosen_prompt







# WOO THE INTRO! <- I should add ascii art!
def intro():
    print("\n" + "="*40)
    print(r"""
  ____  _   _ _   _  ____ _____ ___  _   _ 
 |  _ \| | | | \ | |/ ___| ____/ _ \| \ | |
 | | | | | | |  \| | |  _|  _|| | | |  \| |
 | |_| | |_| | |\  | |_| | |__| |_| | |\  |
 |____/ \___/|_|_\_|\____|_____\___/|_| \_|
  / ___|  / \  |  \/  | ____|              
 | |  _  / _ \ | |\/| |  _|                
 | |_| |/ ___ \| |  | | |___               
  \____/_/   \_\_|  |_|_____|              
 
          """)
    print("Welcome to the dungeon.\n")
    print("You should start by looking around, or maybe checking your inventory.\n")
    print("="*40 + "\n")

# boilerplate player action function
def player_action():
    prompt = get_prompt()
    player_action = input(prompt).strip().lower()
    return player_action

# quitting is fine
def quit_game():
    print("\n" + "="*40)
    print("Goodbye, brave adventurer!")
    print("="*40 + "\n")
    sys.exit()

# yeah, stop typing weird things
def unknown_word():
    print("\n" + "="*40)
    print("I don't understand that word.")
    print("="*40 + "\n")

# this should help restric movement to only valid exits
def move(direction):
    current_room = rooms[player.location]
    if direction in current_room.exits:
        next_room_name = current_room.exits[direction]
        next_room = rooms[next_room_name]
        if next_room.is_locked(player.inventory):
            print("\n" + "="*40)
            print(f"You need the {next_room.key} to enter this room.")
            print("="*40 + "\n")
        else:
            player.location = next_room_name
            print("\n" + "="*40)
            print(f"You move {direction}.")
            print("="*40 + "\n")
            next_room.describe()
    else:
        print("\n" + "="*40)
        print("You can't go that way.")
        print("="*40 + "\n")


# why
def move_north():
    move("north")

# even
def move_south():
    move("south")

# comment
def move_east():
    move("east")

# these
def move_west():
    move("west")

def show_inventory():
    player.show_inventory()

# This is a nightmare - I am losing my mind
def pick_up(item=None):
    current_room = rooms[player.location]

    if not item:  # No item provided
        print("\n" + "=" * 40)
        print("What do you want to pick up? Please type the full name of the item.")
        print("=" * 40 + "\n")
        return  # Exit the function early

    item = item.strip().lower()  # Normalize the item name
    normalized_items = [i.lower() for i in current_room.items]

    if item in normalized_items:
        actual_item = current_room.items.pop(normalized_items.index(item))  # Remove from room
        player.add_to_inventory(actual_item)  # Add to player's inventory
        print("\n" + "=" * 40)
        print(f"You picked up the {actual_item}.")
        print("=" * 40 + "\n")
    else:
        print("\n" + "=" * 40)
        print("You don't see that here.")
        print("=" * 40 + "\n")


# this will let you look at items again, in case you forgot what they were
def examine():
    print("\n" + "="*40)
    if player.inventory:
        for item in player.inventory:
            if item in items:
                print(f"{item}: {items[item]['description']}")
            else:
                print(f"{item}: No description available.")
    else:
        print("You have nothing to examine.")
    print("="*40 + "\n")

# I hate this part
def normalize_command(command):
    """Normalize synonyms into a single standard command."""
    synonyms = {
        "pick up": "pick",
        "get": "pick",
        "grab": "pick",
    }
    return synonyms.get(command, command)  # Return normalized command or itself

# and everything here is evil
multi_word_commands = {"pick up", }  # Add other multi-word commands as needed

# yep, this too
def parse_action(action):
    """Parse the action into a command and argument."""
    words = action.lower().strip().split()  # Split input into words
    if not words:
        return None, None  # Handle empty input gracefully

    # Check for multi-word commands
    for length in range(2, len(words) + 1):  # Try multi-word combinations
        command = " ".join(words[:length])
        if command in multi_word_commands:
            return normalize_command(command), " ".join(words[length:])  # Split command and argument

    # Default: First word is the command, rest is the argument
    return normalize_command(words[0]), " ".join(words[1:])

def show_help():
    print("\n" + "="*40)
    print("You can type the following commands:")
    for command in commands:
        print(f"- {command}")
    print("="*40 + "\n")

# everyone needs debug commands
def debug():
    print("\n" + "="*40)
    print(f"Location: {player.location}")
    print(f"Inventory: {player.inventory}")
    print("="*40 + "\n")

# lets make a commands dictionary - this seems to work and is easy to edit later
commands = {
    "quit": quit_game,
    "q": quit_game,
    "exit": quit_game,
    "inventory": show_inventory,
    "inv": show_inventory,
    "north": move_north,
    "n": move_north,
    "south": move_south,
    "s": move_south,
    "east": move_east,
    "e": move_east,
    "west": move_west,
    "w": move_west,
    "debug": debug,
    "examine": examine,
    "help": show_help,
    "look": room_desc,
    "pick": pick_up, # this...should work?
}



def game_loop():
    intro()
    room_desc()
    while True:
        action = player_action()
        command, argument = parse_action(action)
        if command in commands:
            try:
                if argument:
                    commands[command](argument)
                else:
                    commands[command]()
            except TypeError:
                print("\n" + "="*40)
                print(f"The command '{command}' requires additional input. Please try again.")
                print("="*40 + "\n")
        else:
            unknown_word()


# This starts the actual game
game_loop()
