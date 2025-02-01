def print_room_exits(rooms):
    print("\n=== Room Exits ===")
    for room_coords, room in rooms.items():
        print(f"{room_coords}:")
        for direction, exit_data in room.exits.items():
            lock_status = "LOCKED" if exit_data["locked"] else "unlocked"
            key_name = exit_data["key"] if exit_data["key"] else "None"
            print(f"  {direction} -> {exit_data['room']} [{lock_status}, key: {key_name}]")
    print("===================")

def print_key_placement(rooms):
    print("\n=== Key Placement ===")
    for room_coords, room in rooms.items():
        key_list = [item.name for item in room.items if "key" in item.name]
        if key_list:
            print(f"{room_coords} contains: {', '.join(key_list)}")
    print("===================")

def print_room_items(rooms):
    print("\n=== Room Items ===")
    for room_coords, room in rooms.items():
        item_list = [item.name for item in room.items]
        if item_list:
            print(f"{room_coords} contains: {', '.join(item_list)}")
    print("===================")

def print_player_inventory(player):
    print("\n=== Player Inventory ===")
    if not player.inventory:
        print("The player's inventory is empty.")
    else:
        for item in player.inventory:
            print(f"- {item.name}")
    print("===================")

def check_room_connectivity(dungeon):
    print("\n=== Room Connectivity ===")
    if dungeon.is_dungeon_fully_connected():
        print("All rooms are connected.")
    else:
        print("Some rooms are not connected.")
    print("===================")

def check_key_distribution(dungeon):
    print("\n=== Key Distribution ===")
    key_counts = {room_coords: len([item for item in room.items if "key" in item.name]) for room_coords, room in dungeon.rooms.items()}
    for room_coords, count in key_counts.items():
        print(f"{room_coords} has {count} key(s).")
    print("===================")

def list_locked_doors(dungeon):
    print("\n=== Locked Doors ===")
    for room_coords, room in dungeon.rooms.items():
        for direction, exit_data in room.exits.items():
            if exit_data["locked"]:
                print(f"{room_coords} -> {exit_data['room']} [{direction}] requires {exit_data['key']}")
    print("===================")

def print_room_descriptions(rooms):
    print("\n=== Room Descriptions ===")
    for room_coords, room in rooms.items():
        print(f"{room_coords}: {room.description}")
    print("===================")

def print_exit_phrase(dungeon):
    print("\n=== Exit Phrase ===")
    print(f"Exit Phrase: {dungeon.exit_phrase}")
    print("===================")

def print_clues(dungeon):
    print("\n=== Clues ===")
    for room_coords, room in dungeon.rooms.items():
        clue_list = [item.name for item in room.items if item.name.startswith("clue:")]
        if clue_list:
            print(f"{room_coords} contains clues: {', '.join(clue_list)}")
    print("===================")

def debug_dungeon(dungeon, player):
    print_room_exits(dungeon.rooms)
    print_key_placement(dungeon.rooms)
    print_room_items(dungeon.rooms)
    print_player_inventory(player)
    check_room_connectivity(dungeon)
    check_key_distribution(dungeon)
    list_locked_doors(dungeon)
    print_room_descriptions(dungeon.rooms)
    print_exit_phrase(dungeon)
    print_clues(dungeon)
