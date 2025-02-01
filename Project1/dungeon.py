import random
from room import Room
from item import Item
from debug import debug_dungeon  # Import debug function
from names import ROOM_NAMES, generate_room_name, generate_key_name, generate_exit_phrase  # Import name generation functions

class Dungeon:
    def __init__(self, size=3):  # Default to 3x3 but expandable
        self.grid_size = size
        self.rooms = {}
        self.extra_exit_row = True  # Set to False for an extra column instead
        self.keys_to_place = {}  # Track keys that need to be placed
        self.exit_phrase = ""  # Store the exit phrase

    def generate_rooms(self):
        """Generate a structured dungeon layout."""
        self.create_grid()
        self.connect_rooms_randomly()
        self.ensure_full_connectivity()
        self.place_exit()
        self.lock_doors_and_place_keys()
        self.generate_exit_phrase()  # Generate the exit phrase
        self.scatter_clues()  # Scatter clues in random rooms

    def create_grid(self):
        """Creates a grid of rooms, with an extra exit room outside the grid."""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                room_name = generate_room_name()
                description = f"You are in {room_name}."
                self.rooms[f"Room {row}-{col}"] = Room(description=description, items=[], exits={}, key=None)

        self.add_extra_exit_room()

    def add_extra_exit_room(self):
        """Adds an extra exit room outside the grid."""
        if self.extra_exit_row:
            exit_room = f"Room {self.grid_size}-{self.grid_size//2}"  # Middle of extra row
        else:
            exit_room = f"Room {self.grid_size//2}-{self.grid_size}"  # Middle of extra column

        self.rooms[exit_room] = Room(description="A mysterious chamber with an exit.", items=[], exits={}, key=None)
        self.exit_room = exit_room

    def connect_rooms_randomly(self):
        """Randomly connects rooms with exits."""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                room_name = f"Room {row}-{col}"
                self.connect_room(room_name, row, col)

        # Connect the extra exit room to the grid
        if self.extra_exit_row:
            exit_room = f"Room {self.grid_size}-{self.grid_size//2}"
            grid_room = f"Room {self.grid_size-1}-{self.grid_size//2}"
            self.add_exit(exit_room, grid_room, "north", "south")
        else:
            exit_room = f"Room {self.grid_size//2}-{self.grid_size}"
            grid_room = f"Room {self.grid_size//2}-{self.grid_size-1}"
            self.add_exit(exit_room, grid_room, "west", "east")

    def connect_room(self, room_name, row, col):
        """Connects a single room to its adjacent neighbors with some randomness."""
        if row > 0 and random.choice([True, False]):  # Randomly decide to connect to the room above
            self.add_exit(room_name, f"Room {row-1}-{col}", "north", "south")
        if row < self.grid_size - 1 and random.choice([True, False]):  # Randomly decide to connect to the room below
            self.add_exit(room_name, f"Room {row+1}-{col}", "south", "north")
        if col > 0 and random.choice([True, False]):  # Randomly decide to connect to the room to the left
            self.add_exit(room_name, f"Room {row}-{col-1}", "west", "east")
        if col < self.grid_size - 1 and random.choice([True, False]):  # Randomly decide to connect to the room to the right
            self.add_exit(room_name, f"Room {row}-{col+1}", "east", "west")

    def add_exit(self, room_a, room_b, dir_a, dir_b):
        """Adds a bidirectional exit between two rooms."""
        self.rooms[room_a].exits[dir_a] = {"room": room_b, "locked": False, "key": None}
        self.rooms[room_b].exits[dir_b] = {"room": room_a, "locked": False, "key": None}

    def ensure_full_connectivity(self):
        """Ensures that all rooms are connected and accessible."""
        while not self.is_dungeon_fully_connected():
            room_a, room_b = random.sample(list(self.rooms.keys()), 2)
            possible_directions = [("north", "south"), ("south", "north"), ("east", "west"), ("west", "east")]
            dir_a, dir_b = random.choice(possible_directions)
            self.add_exit(room_a, room_b, dir_a, dir_b)

    def place_exit(self):
        """Places the exit in the extra room, ensuring a long enough path."""
        start_room = self.get_starting_room()
        min_distance = self.grid_size  # Require at least grid_size steps

        while self.get_distance(start_room, self.exit_room) < min_distance or self.exit_room == start_room:
            self.exit_room = random.choice(list(self.rooms.keys()))  # Re-randomize exit placement

        self.rooms[self.exit_room].description += " This room contains the exit!"

    def lock_doors_and_place_keys(self):
        """Locks some doors and places keys in accessible rooms."""
        start_room = self.get_starting_room()
        reachable_rooms = self.get_reachable_rooms(start_room)

        for room in reachable_rooms:
            for direction, exit_data in room.exits.items():
                if random.random() < 0.25:  # 25% chance to lock a door
                    room_description = self.rooms[exit_data["room"]].description
                    if "You are in " in room_description:
                        room_name = room_description.split("You are in ")[1].strip(".")
                        key_name = generate_key_name(room_name)
                        exit_data["locked"] = True
                        exit_data["key"] = key_name
                        self.keys_to_place[exit_data["room"]] = key_name

        self.place_keys_in_reachable_rooms(start_room)

    def place_keys_in_reachable_rooms(self, start_room):
        """Places all keys in reachable rooms."""
        reachable_rooms = self.get_reachable_rooms(start_room)
        valid_rooms = [r for r in reachable_rooms if not any(item.name.startswith("key to") for item in r.items)]
        
        # Shuffle the valid rooms to ensure more even distribution
        random.shuffle(valid_rooms)
        
        for room, key_name in self.keys_to_place.items():
            if valid_rooms:
                chosen_room = valid_rooms.pop(0)  # Take the first room from the shuffled list
                chosen_room.items.append(Item(name=key_name, description=f"A mysterious key labeled '{key_name}'"))

    def generate_exit_phrase(self):
        """Generates and stores the exit phrase."""
        self.exit_phrase = generate_exit_phrase(self.grid_size)

    def scatter_clues(self):
        """Scatters clues for the exit phrase in random rooms."""
        phrase_words = self.exit_phrase.split()
        reachable_rooms = self.get_reachable_rooms(self.get_starting_room())
        valid_rooms = [r for r in reachable_rooms if r != self.exit_room]  # Exclude the exit room

        # Shuffle the valid rooms to ensure more even distribution
        random.shuffle(valid_rooms)

        for word in phrase_words:
            if valid_rooms:
                chosen_room = valid_rooms.pop(0)  # Take the first room from the shuffled list
                clue_item = Item(name=f"clue: {word}", description=f"A clue with the word '{word}'")
                chosen_room.items.append(clue_item)

    def get_reachable_rooms(self, start_room):
        """Returns a list of rooms reachable from the given starting room."""
        from collections import deque

        queue = deque([start_room])
        visited = set()
        reachable_rooms = []

        while queue:
            room_name = queue.popleft()
            if room_name in visited:
                continue
            visited.add(room_name)
            reachable_rooms.append(self.rooms[room_name])

            for exit_data in self.rooms[room_name].exits.values():
                if exit_data["room"] not in visited:
                    queue.append(exit_data["room"])

        return reachable_rooms

    def get_distance(self, start, target):
        """Finds the shortest path distance between two rooms using BFS."""
        from collections import deque

        queue = deque([(start, 0)])  # (current_room, distance)
        visited = set()

        while queue:
            room, distance = queue.popleft()
            if room == target:
                return distance  # Return distance when we reach the target
            if room in visited:
                continue
            visited.add(room)

            for exit_data in self.rooms[room].exits.values():
                queue.append((exit_data["room"], distance + 1))

        return float("inf")  # If no path exists (shouldn't happen)

    def is_dungeon_fully_connected(self):
        """Check if all rooms are reachable from the starting room."""
        visited = set()
        
        # Start from the first room
        start_room = list(self.rooms.keys())[0]
        
        def visit(room_name):
            if room_name in visited:
                return
            visited.add(room_name)
            for exit_data in self.rooms[room_name].exits.values():
                visit(exit_data["room"])

        # Perform flood fill from the starting room
        visit(start_room)

        return len(visited) == len(self.rooms)  # True if all rooms were visited
    
    def get_starting_room(self):
        return list(self.rooms.keys())[0]
