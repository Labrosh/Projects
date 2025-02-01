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
        self.create_room_connections()  # Establish room connections
        self.ensure_connectivity()  # Ensure all rooms are reachable
        self.place_exit()
        self.lock_doors_and_place_keys()
        self.exit_phrase = generate_exit_phrase(self.grid_size)  # Generate the exit phrase
        self.scatter_clues()  # Scatter clues in random rooms

    def create_grid(self):
        """Creates a grid of rooms, with an extra exit room outside the grid."""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                room_name = generate_room_name()
                description = f"You are in {room_name}."
                self.rooms[(row, col)] = Room(description=description, x=row, y=col, items=[], exits={}, key=None)

        self.add_extra_exit_room()

    def add_extra_exit_room(self):
        """Adds an extra exit room outside the grid."""
        exit_room_coords = self.get_extra_exit_room_coords()
        self.rooms[exit_room_coords] = Room(description="A mysterious chamber with an exit.", x=exit_room_coords[0], y=exit_room_coords[1], items=[], exits={}, key=None)
        self.exit_room = self.rooms[exit_room_coords]

    def get_extra_exit_room_coords(self):
        """Returns the coordinates for the extra exit room."""
        if self.extra_exit_row:
            return (self.grid_size, self.grid_size // 2)  # Middle of extra row
        else:
            return (self.grid_size // 2, self.grid_size)  # Middle of extra column

    def create_room_connections(self):
        """Establish valid connections between adjacent rooms, with optional skips for sparse connections."""
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                current_room = self.rooms[(x, y)]
                self.add_random_connections(current_room, x, y)

    def add_random_connections(self, current_room, x, y):
        """Adds random connections to the current room."""
        if (x > 0 and random.random() > 0.3):  # Connect west (70% chance)
            self.add_connection(current_room, (x - 1, y), "west")
        if (x < self.grid_size - 1 and random.random() > 0.3):  # Connect east
            self.add_connection(current_room, (x + 1, y), "east")
        if (y > 0 and random.random() > 0.3):  # Connect north
            self.add_connection(current_room, (x, y - 1), "north")
        if (y < self.grid_size - 1 and random.random() > 0.3):  # Connect south
            self.add_connection(current_room, (x, y + 1), "south")

    def add_connection(self, room_a, room_b_coords, direction):
        """Adds a bidirectional connection between two rooms."""
        opposite_directions = {"north": "south", "south": "north", "east": "west", "west": "east"}
        room_a.exits[direction] = {"room": room_b_coords, "locked": False, "key": None}
        self.rooms[room_b_coords].exits[opposite_directions[direction]] = {"room": (room_a.x, room_a.y), "locked": False, "key": None}

    def ensure_connectivity(self):
        """Ensure all rooms are reachable by connecting isolated rooms."""
        visited = set()

        def dfs(room_coords):
            if room_coords in visited:
                return
            visited.add(room_coords)
            for direction, exit_data in self.rooms[room_coords].exits.items():
                neighbor_coords = exit_data["room"]
                dfs(neighbor_coords)

        # Start DFS from the first room
        start_room_coords = (0, 0)
        dfs(start_room_coords)

        # Add connections to any unvisited room
        for room_coords in self.rooms.keys():
            if room_coords not in visited:
                self.connect_to_closest_visited_room(room_coords, visited)

    def connect_to_closest_visited_room(self, room_coords, visited):
        """Connects the given room to the closest visited room."""
        for direction, neighbor_offset in [("north", (0, -1)), ("south", (0, 1)), ("west", (-1, 0)), ("east", (1, 0))]:
            neighbor_coords = (room_coords[0] + neighbor_offset[0], room_coords[1] + neighbor_offset[1])
            if neighbor_coords in self.rooms and neighbor_coords in visited:
                self.add_connection(self.rooms[room_coords], neighbor_coords, direction)
                break

    def place_exit(self):
        """Places the exit in the extra room, ensuring a long enough path."""
        start_room_coords = self.get_starting_room()
        min_distance = self.grid_size  # Require at least grid_size steps

        while self.get_distance(start_room_coords, (self.exit_room.x, self.exit_room.y)) < min_distance or (self.exit_room.x, self.exit_room.y) == start_room_coords:
            self.exit_room = random.choice(list(self.rooms.values()))  # Re-randomize exit placement

        self.exit_room.description += " This room contains the exit!"

    def lock_doors_and_place_keys(self):
        """Locks some doors and places keys in accessible rooms."""
        start_room_coords = self.get_starting_room()
        reachable_rooms = self.get_reachable_rooms(start_room_coords)

        for room in reachable_rooms:
            self.lock_random_doors(room)

        self.place_keys_in_reachable_rooms(start_room_coords)

    def lock_random_doors(self, room):
        """Locks random doors in the given room."""
        for direction, exit_data in room.exits.items():
            if random.random() < 0.25:  # 25% chance to lock a door
                room_description = self.rooms[exit_data["room"]].description
                if "You are in " in room_description:
                    room_name = room_description.split("You are in ")[1].strip(".")
                    key_name = generate_key_name(room_name)
                    exit_data["locked"] = True
                    exit_data["key"] = key_name
                    self.keys_to_place[exit_data["room"]] = key_name

    def place_keys_in_reachable_rooms(self, start_room_coords):
        """Places all keys in reachable rooms."""
        reachable_rooms = self.get_reachable_rooms(start_room_coords)
        valid_rooms = [r for r in reachable_rooms if not any(item.name.startswith("key to") for item in r.items)]
        
        # Shuffle the valid rooms to ensure more even distribution
        random.shuffle(valid_rooms)
        
        for room_coords, key_name in self.keys_to_place.items():
            if valid_rooms:
                chosen_room = valid_rooms.pop(0)  # Take the first room from the shuffled list
                chosen_room.items.append(Item(name=key_name, description=f"A mysterious key labeled '{key_name}'"))

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

    def get_reachable_rooms(self, start_room_coords):
        """Returns a list of rooms reachable from the given starting room."""
        from collections import deque

        queue = deque([start_room_coords])
        visited = set()
        reachable_rooms = []

        while queue:
            room_coords = queue.popleft()
            if room_coords in visited:
                continue
            visited.add(room_coords)
            reachable_rooms.append(self.rooms[room_coords])

            for exit_data in self.rooms[room_coords].exits.values():
                if exit_data["room"] not in visited:
                    queue.append(exit_data["room"])

        return reachable_rooms

    def get_distance(self, start_coords, target_coords):
        """Finds the shortest path distance between two rooms using BFS."""
        from collections import deque

        queue = deque([(start_coords, 0)])  # (current_room_coords, distance)
        visited = set()

        while queue:
            room_coords, distance = queue.popleft()
            if room_coords == target_coords:
                return distance  # Return distance when we reach the target
            if room_coords in visited:
                continue
            visited.add(room_coords)

            for exit_data in self.rooms[room_coords].exits.values():
                queue.append((exit_data["room"], distance + 1))

        return float("inf")  # If no path exists (shouldn't happen)

    def is_dungeon_fully_connected(self):
        """Check if all rooms are reachable from the starting room."""
        visited = set()
        
        # Start from the first room
        start_room_coords = (0, 0)
        
        def visit(room_coords):
            if room_coords in visited:
                return
            visited.add(room_coords)
            for exit_data in self.rooms[room_coords].exits.values():
                visit(exit_data["room"])

        # Perform flood fill from the starting room
        visit(start_room_coords)

        return len(visited) == len(self.rooms)  # True if all rooms were visited
    
    def get_starting_room(self):
        return (0, 0)  # Return the coordinates of the starting room
