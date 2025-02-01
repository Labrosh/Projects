class Player:
    def __init__(self, starting_room_coords):
        self.location = starting_room_coords  # Store location as coordinates
        self.inventory = []

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def show_inventory(self):
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("You have the following items:")
            for item in self.inventory:
                print(f"- {item.name}")
