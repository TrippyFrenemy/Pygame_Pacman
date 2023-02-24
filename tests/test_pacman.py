import unittest

try:
    from startgame import GameController
    module_failed = False
except ImportError:
    module_failed = True


# In console: python -m unittest -v tests/test_pacman.py
class TestController(unittest.TestCase):
    def setUp(self):
        if module_failed:
            self.skipTest('module doesnt exist')
        self.start = GameController()
        self.start.startGame()

    def test_background(self):
        self.start.setBackground()

    def test_update(self):
        self.start.update()

    def test_checkEvents(self):
        self.start.checkEvents()
        self.start.checkGhostEvents()
        self.start.checkPelletEvents()
        self.start.checkFruitEvents()

    def test_entities(self):
        self.start.showEntities()
        self.start.hideEntities()

    def test_updatescore(self):
        self.start.update()

    def test_restartgame(self):
        self.start.restartGame()

    def test_resetLevel(self):
        self.start.resetLevel()

    def test_nextLevel(self):
        self.start.nextLevel()

    def test_render(self):
        self.start.render()


if __name__ == "__main__":
    unittest.main()
