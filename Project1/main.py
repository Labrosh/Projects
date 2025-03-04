from game import Game
from player import Player
from room import Room
from item import Item, items
from dungeon import Dungeon

dungeon = Dungeon(size=5)
dungeon.generate_rooms()

rooms = dungeon.rooms
starting_room_coords = (0, 0)
player = Player(starting_room_coords)
game = Game(player, rooms, dungeon)
game.game_loop()
