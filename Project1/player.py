class Player:
    def __init__(self, starting_room):
        self.location = starting_room
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
