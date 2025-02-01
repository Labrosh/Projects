def print_room_exits(rooms):
    """Print room exits to check if any are locked."""
    print("\n=== Room Exits ===")
    for room_name, room in rooms.items():
        print(f"{room_name}:")
        for direction, exit_data in room.exits.items():
            lock_status = "LOCKED" if exit_data["locked"] else "unlocked"
            key_name = exit_data["key"] if exit_data["key"] else "None"
            print(f"  {direction} -> {exit_data['room']} [{lock_status}, key: {key_name}]")
    print("===================")

def print_key_placement(rooms):
    """Print all rooms with placed keys."""
    print("\n=== Key Placement ===")
    for room_name, room in rooms.items():
        key_list = [item.name for item in room.items if "key" in item.name]
        if key_list:
            print(f"{room_name} contains: {', '.join(key_list)}")
    print("===================")

def print_room_items(rooms):
    """Print all items in each room."""
    print("\n=== Room Items ===")
    for room_name, room in rooms.items():
        item_list = [item.name for item in room.items]
        if item_list:
            print(f"{room_name} contains: {', '.join(item_list)}")
    print("===================")

def print_player_inventory(player):
    """Print the player's inventory."""
    print("\n=== Player Inventory ===")
    if not player.inventory:
        print("The player's inventory is empty.")
    else:
        for item in player.inventory:
            print(f"- {item.name}")
    print("===================")

def check_room_connectivity(dungeon):
    """Check if all rooms are connected."""
    print("\n=== Room Connectivity ===")
    if dungeon.is_dungeon_fully_connected():
        print("All rooms are connected.")
    else:
        print("Some rooms are not connected.")
    print("===================")

def check_key_distribution(dungeon):
    """Check if keys are evenly distributed."""
    print("\n=== Key Distribution ===")
    key_counts = {room_name: len([item for item in room.items if "key" in item.name]) for room_name, room in dungeon.rooms.items()}
    for room_name, count in key_counts.items():
        print(f"{room_name} has {count} key(s).")
    print("===================")

def list_locked_doors(dungeon):
    """List all locked doors and their corresponding keys."""
    print("\n=== Locked Doors ===")
    for room_name, room in dungeon.rooms.items():
        for direction, exit_data in room.exits.items():
            if exit_data["locked"]:
                print(f"{room_name} -> {exit_data['room']} [{direction}] requires {exit_data['key']}")
    print("===================")

def print_room_descriptions(rooms):
    """Print descriptions of all rooms."""
    print("\n=== Room Descriptions ===")
    for room_name, room in rooms.items():
        print(f"{room_name}: {room.description}")
    print("===================")

def debug_dungeon(dungeon, player):
    """Run all debug functions for the dungeon and player."""
    print_room_exits(dungeon.rooms)
    print_key_placement(dungeon.rooms)
    print_room_items(dungeon.rooms)
    print_player_inventory(player)
    check_room_connectivity(dungeon)
    check_key_distribution(dungeon)
    list_locked_doors(dungeon)
    print_room_descriptions(dungeon.rooms)
