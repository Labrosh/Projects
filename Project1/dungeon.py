import random
from room import Room
from item import Item  

class Dungeon:
    def __init__(self, size=5):
        self.size = size
        self.rooms = {}

    def generate_rooms(self): 
        for i in range(self.size):
            room_name = f"Room {i + 1}"
            description = f"You are in {room_name}."
            self.rooms[room_name] = Room(description=description, items=[], exits={}, key=None)
        room_names = list(self.rooms.keys())

        for i in range(len(room_names) - 1):
            self.rooms[room_names[i]].exits["east"] = {
                "room": room_names[i + 1],
                "locked": random.choice([True, False]),  # Randomly decide if locked
                "key": None  # No key needed by default
            }
            self.rooms[room_names[i + 1]].exits["west"] = {
                "room": room_names[i],
                "locked": False,
                "key": None
            }
        
        # Ensure at least one exit is always unlocked
        self.rooms[room_names[0]].exits["east"]["locked"] = False

        for room in self.rooms.values():
            print(f"{room.description} has exits: {room.exits}")
        
        room_list = list(self.rooms.values())  # Convert dictionary to a list of rooms

        for i, room in enumerate(room_list):
            for direction, exit_data in room.exits.items():
                if exit_data["locked"]:  # If the door is locked
                    key_name = f"key to {exit_data['room']}"  # Name the key
                    exit_data["key"] = key_name  # Assign key to door

                    # Place the key in a previous room (if possible)
                    if i > 0:
                        room_list[i - 1].items.append(Item(name=key_name, description=f"A key that unlocks {exit_data['room']}."))

        print("Keys placed and doors locked!")

        exit_room_name = random.choice(list(self.rooms.keys()))  # Randomly pick any room
        self.rooms[exit_room_name].description += " This room contains the exit!"
        self.exit_room = exit_room_name  # Store the exit for later checking
    
    def get_starting_room(self):
        return list(self.rooms.keys())[0]
