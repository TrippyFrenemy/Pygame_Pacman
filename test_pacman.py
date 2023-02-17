import unittest

from run import GameController

class TestController(unittest.TestCase):
    def setUp(self):
        self.start = GameController()

    def test_startgame(self):
        self.start.startGame()

if __name__ == "__main__":
    unittest.main()