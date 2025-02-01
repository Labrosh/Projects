from names import item_names  # Import item names from names.py

class Item:
    def __init__(self, name, description):
        self.name = name.lower()  # Store item names in lowercase
        self.description = description

    def describe(self):
        print(f"{self.name}: {self.description}")

items = {name: Item(name=name, description=f"A description for {name}.") for name in item_names}
