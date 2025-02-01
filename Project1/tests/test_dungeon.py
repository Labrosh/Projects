import unittest
from dungeon import Dungeon

class TestDungeon(unittest.TestCase):
    def setUp(self):
        self.dungeon = Dungeon(size=3)
        self.dungeon.generate_rooms()

    def test_dungeon_size(self):
        self.assertEqual(self.dungeon.grid_size, 3)

    def test_rooms_created(self):
        self.assertEqual(len(self.dungeon.rooms), 10)  # 9 grid rooms + 1 extra exit room

    def test_exit_phrase_generated(self):
        self.assertTrue(self.dungeon.exit_phrase)

    def test_dungeon_fully_connected(self):
        self.assertTrue(self.dungeon.is_dungeon_fully_connected())

if __name__ == '__main__':
    unittest.main()
