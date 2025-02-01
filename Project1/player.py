import logging

class Player:
    def __init__(self, starting_room_coords):
        self.location = starting_room_coords
        self.inventory = []

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def show_inventory(self):
        if not self.inventory:
            logging.info("Your inventory is empty.")
        else:
            logging.info("You have the following items:")
            for item in self.inventory:
                logging.info(f"- {item.name}")
