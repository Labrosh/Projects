import random
from room import Room
from item import Item
from debug import debug_dungeon
from names import ROOM_NAMES, generate_room_name, generate_key_name, generate_exit_phrase

class Dungeon:
    def __init__(self, size=3):
        self.grid_size = size
        self.rooms = {}
        self.extra_exit_row = True
        self.keys_to_place = {}
        self.exit_phrase = ""

    def generate_rooms(self):
        self.create_grid()
        self.create_room_connections()
        self.ensure_connectivity()
        self.place_exit()
        self.lock_doors_and_place_keys()
        self.exit_phrase = generate_exit_phrase(self.grid_size)
        self.scatter_clues()

    def create_grid(self):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                room_name = generate_room_name()
                description = f"You are in {room_name}."
                self.rooms[(row, col)] = Room(description=description, x=row, y=col, items=[], exits={}, key=None)
        self.add_extra_exit_room()

    def add_extra_exit_room(self):
        exit_room_coords = self.get_extra_exit_room_coords()
        self.rooms[exit_room_coords] = Room(description="A mysterious chamber with an exit.", x=exit_room_coords[0], y=exit_room_coords[1], items=[], exits={}, key=None)
        self.exit_room = self.rooms[exit_room_coords]

    def get_extra_exit_room_coords(self):
        if self.extra_exit_row:
            return (self.grid_size, self.grid_size // 2)
        else:
            return (self.grid_size // 2, self.grid_size)

    def create_room_connections(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                current_room = self.rooms[(x, y)]
                self.add_random_connections(current_room, x, y)

    def add_random_connections(self, current_room, x, y):
        if (x > 0 and random.random() > 0.3):
            self.add_connection(current_room, (x - 1, y), "west")
        if (x < self.grid_size - 1 and random.random() > 0.3):
            self.add_connection(current_room, (x + 1, y), "east")
        if (y > 0 and random.random() > 0.3):
            self.add_connection(current_room, (x, y - 1), "north")
        if (y < self.grid_size - 1 and random.random() > 0.3):
            self.add_connection(current_room, (x, y + 1), "south")

    def add_connection(self, room_a, room_b_coords, direction):
        opposite_directions = {"north": "south", "south": "north", "east": "west", "west": "east"}
        room_a.exits[direction] = {"room": room_b_coords, "locked": False, "key": None}
        self.rooms[room_b_coords].exits[opposite_directions[direction]] = {"room": (room_a.x, room_a.y), "locked": False, "key": None}

    def ensure_connectivity(self):
        visited = set()

        def dfs(room_coords):
            if room_coords in visited:
                return
            visited.add(room_coords)
            for direction, exit_data in self.rooms[room_coords].exits.items():
                neighbor_coords = exit_data["room"]
                dfs(neighbor_coords)

        start_room_coords = (0, 0)
        dfs(start_room_coords)

        for room_coords in self.rooms.keys():
            if room_coords not in visited:
                self.connect_to_closest_visited_room(room_coords, visited)

    def connect_to_closest_visited_room(self, room_coords, visited):
        for direction, neighbor_offset in [("north", (0, -1)), ("south", (0, 1)), ("west", (-1, 0)), ("east", (1, 0))]:
            neighbor_coords = (room_coords[0] + neighbor_offset[0], room_coords[1] + neighbor_offset[1])
            if neighbor_coords in self.rooms and neighbor_coords in visited:
                self.add_connection(self.rooms[room_coords], neighbor_coords, direction)
                break

    def place_exit(self):
        start_room_coords = self.get_starting_room()
        min_distance = self.grid_size

        while self.get_distance(start_room_coords, (self.exit_room.x, self.exit_room.y)) < min_distance or (self.exit_room.x, self.exit_room.y) == start_room_coords:
            self.exit_room = random.choice(list(self.rooms.values()))

        self.exit_room.description += " This room contains the exit!"

    def lock_doors_and_place_keys(self):
        start_room_coords = self.get_starting_room()
        reachable_rooms = self.get_reachable_rooms(start_room_coords)

        for room in reachable_rooms:
            self.lock_random_doors(room)

        self.place_keys_in_reachable_rooms(start_room_coords)

    def lock_random_doors(self, room):
        for direction, exit_data in room.exits.items():
            if random.random() < 0.25:
                room_description = self.rooms[exit_data["room"]].description
                if "You are in " in room_description:
                    room_name = room_description.split("You are in ")[1].strip(".")
                    key_name = generate_key_name(room_name)
                    exit_data["locked"] = True
                    exit_data["key"] = key_name
                    self.keys_to_place[exit_data["room"]] = key_name

    def place_keys_in_reachable_rooms(self, start_room_coords):
        reachable_rooms = self.get_reachable_rooms(start_room_coords)
        valid_rooms = [r for r in reachable_rooms if not any(item.name.startswith("key to") for item in r.items)]
        random.shuffle(valid_rooms)
        
        for room_coords, key_name in self.keys_to_place.items():
            if valid_rooms:
                chosen_room = valid_rooms.pop(0)
                chosen_room.items.append(Item(name=key_name, description=f"A mysterious key labeled '{key_name}'"))

    def scatter_clues(self):
        phrase_words = self.exit_phrase.split()
        reachable_rooms = self.get_reachable_rooms(self.get_starting_room())
        valid_rooms = [r for r in reachable_rooms if r != self.exit_room]
        random.shuffle(valid_rooms)

        for word in phrase_words:
            if valid_rooms:
                chosen_room = valid_rooms.pop(0)
                clue_item = Item(name=f"clue: {word}", description=f"A clue with the word '{word}'")
                chosen_room.items.append(clue_item)

    def get_reachable_rooms(self, start_room_coords):
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
        from collections import deque

        queue = deque([(start_coords, 0)])
        visited = set()

        while queue:
            room_coords, distance = queue.popleft()
            if room_coords == target_coords:
                return distance
            if room_coords in visited:
                continue
            visited.add(room_coords)

            for exit_data in self.rooms[room_coords].exits.values():
                queue.append((exit_data["room"], distance + 1))

        return float("inf")

    def is_dungeon_fully_connected(self):
        visited = set()
        start_room_coords = (0, 0)
        
        def visit(room_coords):
            if room_coords in visited:
                return
            visited.add(room_coords)
            for exit_data in self.rooms[room_coords].exits.values():
                visit(exit_data["room"])

        visit(start_room_coords)

        return len(visited) == len(self.rooms)
    
    def get_starting_room(self):
        return (0, 0)
