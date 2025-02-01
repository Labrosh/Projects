from game import Game
from player import Player
from room import Room
from item import Item, items
from dungeon import Dungeon

dungeon = Dungeon(size=5)
dungeon.generate_rooms()
rooms = dungeon.rooms

starting_room = dungeon.get_starting_room()
player = Player(starting_room)
game = Game(player, rooms, dungeon)  # Pass dungeon to Game
game.game_loop()
