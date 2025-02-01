import sys
import random
from player import Player
from room import Room
from item import Item

class Game:
    def __init__(self, player, rooms):
        self.player = player
        self.rooms = rooms
        self.recent_prompts = []
        self.commands = {
            "quit": self.quit_game,
            "q": self.quit_game,
            "exit": self.quit_game,
            "inventory": self.show_inventory,
            "inv": self.show_inventory,
            "north": lambda: self.move("north"),
            "n": lambda: self.move("north"),
            "south": lambda: self.move("south"),
            "s": lambda: self.move("south"),
            "east": lambda: self.move("east"),
            "e": lambda: self.move("east"),
            "west": lambda: self.move("west"),
            "w": lambda: self.move("west"),
            "debug": self.debug,
            "examine": self.examine,
            "help": self.show_help,
            "look": self.room_desc,
            "pick": self.pick_up,
        }

    def handle_command(self, command, argument=None):
        if command in self.commands:
            try:
                if argument:
                    self.commands[command](argument)
                else:
                    self.commands[command]()
            except TypeError:
                self.print_block(f"The command '{command}' requires additional input. Please try again.")
        else:
            self.unknown_word()

    def print_block(self, message):
        print("\n" + "="*40)
        print(message)
        print("="*40 + "\n")

    def room_desc(self):
        room = self.rooms[self.player.location]
        location_header = f"Location: {self.player.location.upper()}"
        room_description = room.describe()
        self.print_block(f"{location_header}\n\n{room_description}")

    def get_prompt(self):
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
            "Ah...this again. What's your next move? ",
            "Couldn't think of anything better? What's your next move? ",
            "Bored yet? What's your next move? ",
            "I'm getting tired of this. What's your next move? ",
            "I could have guessed that. What's your next move? ",
            "I'm not impressed. What's your next move? ",
            "I'm not amused. What's your next move? ",
            "*Yawn* What's your next move? ",
            "You're not very creative. What's your next move? ",
        ]
        available_prompts = [p for p in prompts if p not in self.recent_prompts]

        if not available_prompts:
            self.recent_prompts.clear()
            available_prompts = prompts

        chosen_prompt = random.choice(available_prompts)

        self.recent_prompts.append(chosen_prompt)
        if len(self.recent_prompts) > 5:
            self.recent_prompts.pop(0)

        return chosen_prompt

    def intro(self):
        self.print_block(r"""
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
        self.print_block("Welcome to the dungeon.\nYou should start by looking around, or maybe checking your inventory.")

    def player_action(self):
        prompt = self.get_prompt()
        return input(prompt).strip().lower()

    def quit_game(self):
        self.print_block("Goodbye, brave adventurer!")
        sys.exit()

    def unknown_word(self):
        self.print_block("I don't understand that word.")

    def move(self, direction):
        current_room = self.rooms[self.player.location]
        if direction in current_room.exits:
            next_room_name = current_room.exits[direction]
            next_room = self.rooms[next_room_name]
            if next_room.is_locked(self.player.inventory):
                self.print_block(f"You need the {next_room.key} to enter this room.")
            else:
                self.player.location = next_room_name
                self.print_block(f"You move {direction}.")
                self.room_desc()
        else:
            self.print_block("You can't go that way.")

    def show_inventory(self):
        self.player.show_inventory()

    def pick_up(self, item_name=None):
        current_room = self.rooms[self.player.location]

        if not item_name:  # No item provided
            self.print_block("What do you want to pick up? Please type the full name of the item.")
            return

        item = current_room.find_item_by_name(item_name.strip().lower())
        if item:
            current_room.items.remove(item)
            self.player.add_to_inventory(item)
            self.print_block(f"You picked up the {item.name}.")
        else:
            available_items = ", ".join(item.name for item in current_room.items)
            self.print_block(f"You don't see that here. Items in the room: {available_items if available_items else 'None'}")

    def examine(self):
        if self.player.inventory:
            messages = [f"{item.name}: {item.description}" for item in self.player.inventory]
            self.print_block("\n".join(messages))
        else:
            self.print_block("You have nothing to examine.")

    def normalize_command(self, command):
        synonyms = {
            "pick up": "pick",
            "get": "pick",
            "grab": "pick",
        }
        return synonyms.get(command, command)

    def parse_action(self, action):
        words = action.lower().strip().split()
        if not words:
            return None, None

        multi_word_commands = {"pick up"}
        for length in range(2, len(words) + 1):
            command = " ".join(words[:length])
            if command in multi_word_commands:
                return self.normalize_command(command), " ".join(words[length:])

        return self.normalize_command(words[0]), " ".join(words[1:])

    def show_help(self):
        help_message = "You can type the following commands:\n" + "\n".join(f"- {command}" for command in self.commands)
        self.print_block(help_message)

    def debug(self):
        debug_message = f"Location: {self.player.location}\nInventory: {', '.join(item.name for item in self.player.inventory)}"
        self.print_block(debug_message)

    def game_loop(self):
        self.intro()
        self.room_desc()
        while True:
            action = self.player_action()
            command, argument = self.parse_action(action)
            self.handle_command(command, argument)
