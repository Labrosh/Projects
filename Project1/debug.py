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
        key_list = [item.name for item in room.items]
        if key_list:
            print(f"{room_name} contains: {', '.join(key_list)}")
    print("===================")

def debug_dungeon(dungeon):
    """Run all debug functions for the dungeon."""
    print_room_exits(dungeon.rooms)
    print_key_placement(dungeon.rooms)
