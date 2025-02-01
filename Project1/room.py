from names import generate_room_name, generate_key_name  # Import name generation functions

class Room:
    def __init__(self, description, x=None, y=None, items=None, exits=None, key=None):
        self.description = description
        self.x = x  # Add x-coordinate
        self.y = y  # Add y-coordinate
        self.items = items if items else []
        self.exits = exits if exits else {}
        self.key = key

    def describe(self):
        message = self.description
        if self.items:
            message += "\n\nYou see the following items:\n" + "\n".join(f"- {item.name}" for item in self.items)
        return message

    def is_locked(self, player_inventory):
        return self.key and not any(item.name.lower() == self.key.lower() for item in player_inventory)
    
    def find_item_by_name(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():  # Ensure case-insensitive comparison
                return item
        return None
