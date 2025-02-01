class Item:
    def __init__(self, name, description):
        self.name = name.lower()  # Store item names in lowercase
        self.description = description

    def describe(self):
        print(f"{self.name}: {self.description}")

items = {
    "slimy key": Item(
        name="slimy key",
        description="A slimy key that smells of old fish. You found this in the south room."
    ),
    "stone key": Item(
        name="stone key",
        description="A heavy key made of stone. You found this in the north room."
    ),
    "shiny key": Item(
        name="shiny key",
        description="A shiny key that sparkles in the light. You found this in the east room."
    ),
    "ancient key": Item(
        name="ancient key",
        description="An ancient key that looks like it's been around for centuries. You found this in the west room. It seems to be bigger than the other keys you've found."
    )
}
