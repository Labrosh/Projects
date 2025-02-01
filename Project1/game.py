import sys
import random
import matplotlib
import networkx as nx

try:
    import tkinter
    matplotlib.use("TkAgg")
    interactive_backend = True
except ImportError:
    matplotlib.use("Agg")
    interactive_backend = False

import matplotlib.pyplot as plt
from player import Player
from room import Room
from item import Item
from debug import debug_dungeon
from names import prompts, generate_exit_phrase

class Game:
    def __init__(self, player, rooms, dungeon):
        self.player = player
        self.rooms = rooms
        self.dungeon = dungeon
        self.recent_prompts = []
        self.debug_mode = False
        self.commands = self.initialize_commands()

    def initialize_commands(self):
        return {
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
            "map": self.show_map,
            "enable_debug": self.enable_debug,
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
        location_header = f"Location: {self.player.location}"
        room_description = room.describe()
        self.print_block(f"{location_header}\n\n{room_description}")

    def get_prompt(self):
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
            exit_data = current_room.exits[direction]
            next_room_coords = exit_data["room"]

            if exit_data["locked"]:
                required_key = exit_data["key"].lower()
                if any(item.name == required_key for item in self.player.inventory):
                    self.print_block(f"You use the {required_key} to unlock the door.")
                    exit_data["locked"] = False
                else:
                    self.print_block(f"The door is locked. You need the {exit_data['key']} to open it.")
                    return

            self.player.location = next_room_coords
            self.print_block(f"You move {direction}.")
            self.room_desc()

            if self.player.location == (self.dungeon.exit_room.x, self.dungeon.exit_room.y):
                self.prompt_exit_phrase()
        else:
            self.print_block("You can't go that way.")

    def prompt_exit_phrase(self):
        self.print_block("You have reached the exit room. To escape, you must enter the correct exit phrase.")
        entered_phrase = input("Enter the exit phrase: ").strip().lower()
        if entered_phrase == self.dungeon.exit_phrase.lower():
            self.print_block("Congratulations! You have escaped the dungeon!")
            sys.exit()
        else:
            self.print_block("Incorrect phrase. You are still trapped in the dungeon.")

    def show_inventory(self):
        self.player.show_inventory()

    def pick_up(self, item_name=None):
        current_room = self.rooms[self.player.location]

        if not item_name:
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

    def enable_debug(self):
        self.debug_mode = True
        self.print_block("Debug mode enabled.")
        debug_dungeon(self.dungeon, self.player)

    def show_map(self):
        grid_size = self.dungeon.grid_size
        G = nx.Graph()

        for (row, col), room in self.dungeon.rooms.items():
            G.add_node((row, col), pos=(col, -row))

        for (row, col), room in self.dungeon.rooms.items():
            for direction, exit_data in room.exits.items():
                exit_row, exit_col = exit_data["room"]
                if not G.has_edge((row, col), (exit_row, exit_col)):
                    G.add_edge((row, col), (exit_row, exit_col))

        pos = nx.get_node_attributes(G, 'pos')

        plt.figure(figsize=(8, 8))
        nx.draw(G, pos, with_labels=False, node_size=800, node_color="gray", edgecolors="black", font_weight="bold")

        nx.draw_networkx_nodes(G, pos, nodelist=[self.player.location], node_color="red", label="Player")
        nx.draw_networkx_nodes(G, pos, nodelist=[(self.dungeon.exit_room.x, self.dungeon.exit_room.y)], node_color="green", label="Exit")

        for (row, col) in [self.player.location, (self.dungeon.exit_room.x, self.dungeon.exit_room.y)]:
            plt.text(col, -row, "P" if (row, col) == self.player.location else "E",
                     ha='center', va='center', fontsize=12, color="white", fontweight="bold")

        plt.title("Dungeon Map")
        plt.grid(True)
        plt.axis("off")

        if interactive_backend:
            plt.show()
        else:
            plt.savefig("dungeon_map_networkx.png")
            print("Dungeon map saved as dungeon_map_networkx.png")

    def game_loop(self):
        self.intro()
        self.room_desc()
        while True:
            action = self.player_action()
            command, argument = self.parse_action(action)
            self.handle_command(command, argument)
