import random
from room import Room
from item import Item  

class Dungeon:
    def __init__(self, size=5):
        self.size = size
        self.rooms = {}
        self.grid_size = 3  # Changeable later!
        self.extra_exit_row = True  # Set to False for an extra column instead

    def generate_rooms(self):
        """Generate a structured dungeon layout."""
        self.create_grid()
        self.connect_rooms_randomly()
        self.ensure_full_connectivity()
        self.place_keys()
        self.place_exit()
        print("Dungeon generation complete!")

    def create_grid(self):
        """Creates a grid of rooms, with an extra exit room outside the grid."""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                room_name = f"Room {row}-{col}"
                description = f"You are in {room_name}."
                self.rooms[room_name] = Room(description=description, items=[], exits={}, key=None)

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

    def connect_room(self, room_name, row, col):
        """Connects a single room to its neighbors."""
        if row > 0 and random.choice([True, False]):
            self.add_exit(room_name, f"Room {row-1}-{col}", "north", "south")
        if row < self.grid_size - 1 and random.choice([True, False]):
            self.add_exit(room_name, f"Room {row+1}-{col}", "south", "north")
        if col > 0 and random.choice([True, False]):
            self.add_exit(room_name, f"Room {row}-{col-1}", "west", "east")
        if col < self.grid_size - 1 and random.choice([True, False]):
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

    def place_keys(self):
        """Places keys in rooms for locked doors."""
        for room in self.rooms.values():
            for exit_data in room.exits.values():
                if exit_data["locked"]:
                    self.place_key_for_exit(exit_data)

    def place_key_for_exit(self, exit_data):
        """Places a key for a locked exit in a random room."""
        key_name = f"key to {exit_data['room']}"
        exit_data["key"] = key_name
        random.choice(list(self.rooms.values())).items.append(
            Item(name=key_name, description=f"A key that unlocks {exit_data['room']}.")
        )

    def place_exit(self):
        """Places the exit in the extra room, ensuring a long enough path."""
        start_room = self.get_starting_room()
        min_distance = self.grid_size  # Require at least grid_size steps

        while self.get_distance(start_room, self.exit_room) < min_distance or self.exit_room == start_room:
            self.exit_room = random.choice(list(self.rooms.keys()))  # Re-randomize exit placement

        self.rooms[self.exit_room].description += " This room contains the exit!"
        self.lock_exit_room(start_room)

    def lock_exit_room(self, start_room):
        """Locks the exit room and places the key in a suitable room."""
        for room_name, room in self.rooms.items():
            for direction, exit_data in room.exits.items():
                if exit_data["room"] == self.exit_room:
                    exit_data["locked"] = True
                    key_name = f"exit key"
                    exit_data["key"] = key_name
                    # Ensure the key is not placed in the starting room, exit room, or rooms too close to the start
                    possible_rooms = [r for r in self.rooms.values() if self.get_distance(start_room, r.description.split()[2]) > 1 and r != self.rooms[self.exit_room]]
                    random.choice(possible_rooms).items.append(
                        Item(name=key_name, description="A special key that unlocks the exit.")
                    )
                    return  # Stop after locking one door

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
