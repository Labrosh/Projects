import random

item_names = [
    "slimy key",
    "stone key",
    "shiny key",
    "ancient key"
]

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

KEY_DESCRIPTIONS = ["Rusty", "Tarnished", "Bone-Carved", "Ancient", "Eldritch", "Silver", "Iron"]

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

EXIT_PHRASES = [
    "Shadows whisper beyond the abyss",
    "Moonlight fades through silent veils",
    "Ancient fires burn deep within",
    "Lost echoes call for release",
    "Storm winds howl beyond voids",
    "Crimson flames dance beneath stars",
    "Frozen echoes shatter silver mists",
    "Forgotten paths lead to freedom",
    "Eternal twilight lingers within ruins",
    "Cursed whispers guide the way",
    "Darkness falls upon the crypt",
    "Mystic lights flicker in shadows",
    "Haunted spirits roam the halls",
    "Silent screams echo through time",
    "Hidden secrets lie in wait",
    "Ancient guardians watch the gate",
    "Eerie silence fills the air",
    "Ghostly figures drift through walls",
    "Twisted roots choke the path",
    "Winds of fate blow cold",
]

used_room_names = set()
used_key_names = set()

def generate_room_name():
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
    while True:
        key_name = f"{random.choice(KEY_DESCRIPTIONS)} Key to {room_name}"
        if key_name not in used_key_names:
            used_key_names.add(key_name)
            return key_name

def generate_exit_phrase(dungeon_size):
    phrase = random.choice(EXIT_PHRASES)
    words = phrase.split()

    phrase_length = max(3, min(5, dungeon_size))

    if phrase_length == 4:
        trimmed_words = [words[0], words[2], words[3], words[4]]
    elif phrase_length == 3:
        trimmed_words = [words[0], words[2], words[4]]
    else:
        trimmed_words = words

    return " ".join(trimmed_words)
