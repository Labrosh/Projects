from room import Room

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
            self.rooms[room_names[i]].exits["east"] = room_names[i + 1]
            self.rooms[room_names[i + 1]].exits["west"] = room_names[i]
        
        for room in self.rooms.values():
            print(f"{room.description} has exits: {room.exits}")
    
    def get_starting_room(self):
        return list(self.rooms.keys())[0]
