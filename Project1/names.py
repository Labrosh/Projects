import random

# List of item names
item_names = [
    "slimy key",
    "stone key",
    "shiny key",
    "ancient key"
]

# List of possible room names
ROOM_NAMES = [
    "The Shadowed Library", "The Cursed Chamber", "Whispering Hollow",
    "The Forgotten Vault", "The Ancient Shrine", "The Silent Crypt",
    "The Eldritch Gateway", "The Sunken Ruins", "The Obsidian Sanctum",
    "The Forsaken Altar", "The Crumbling Keep", "The Haunted Mausoleum",
    "The Mystic Cavern", "The Enchanted Forest", "The Hidden Grotto",
    "The Abandoned Mine", "The Crystal Cave", "The Dark Abyss",
    "The Fiery Pit", "The Frozen Tundra", "The Golden Hall",
    "The Iron Fortress", "The Jade Temple", "The Lost City",
    "The Mystic Tower", "The Obsidian Fortress", "The Phantom Ship",
    "The Sacred Grove", "The Silver Spire", "The Sunken Temple"
]

# Key description prefixes
KEY_DESCRIPTIONS = ["Rusty", "Tarnished", "Bone-Carved", "Ancient", "Eldritch", "Silver", "Iron"]

# List of prompts
prompts = [
    "What do you want to do? ",
    "What's next? ",
    "What's your next move? ",
    "What's the plan? ",
    "What's the next step? ",
    "The darkness is closing in. What now? ",
    "The walls are closing in. What do you do? ",
    "The shadows are moving. What's your move? ",
    "The silence is deafening. What's next? ",
    "The air is thick with anticipation. What's your next move? ",
    "You feel a chill run down your spine. What do you do? ",
    "You hear a faint whisper. What's your next move? ",
    "You feel a presence watching you. What's your next move? ",
    "You feel a sense of dread. What do you do? ",
    "You feel a sense of foreboding. What's your next move? ",
    "You feel a sense of unease. What do you do? ",
    "Something smells foul. What's your next move? ",
    "You hear a faint rustling. What's your next move? ",
    "You hear a faint creaking. What do you do? ",
    "Nice one, adventurer, but what's next? ",
    "Ah...this again. What's your next move? ",
    "Couldn't think of anything better? What's your next move? ",
    "Bored yet? What's your next move? ",
    "I'm getting tired of this. What's your next move? ",
    "I could have guessed that. What's your next move? ",
    "I'm not impressed. What's your next move? ",
    "I'm not amused. What's your next move? ",
    "*Yawn* What's your next move? ",
    "You're not very creative. What's your next move? ",
]

used_room_names = set()
used_key_names = set()

def generate_room_name():
    """Returns a random thematic name for a dungeon room, ensuring uniqueness."""
    available_names = set(ROOM_NAMES) - used_room_names
    if available_names:
        room_name = random.choice(list(available_names))
        used_room_names.add(room_name)
        return room_name
    else:
        room_name = f"Generated Room {len(used_room_names) + 1}"
        used_room_names.add(room_name)
        return room_name

def generate_key_name(room_name):
    """Creates a unique key name based on the room it unlocks, ensuring uniqueness."""
    while True:
        key_name = f"{random.choice(KEY_DESCRIPTIONS)} Key to {room_name}"
        if key_name not in used_key_names:
            used_key_names.add(key_name)
            return key_name
