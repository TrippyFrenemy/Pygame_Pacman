import unittest

try:
    from src.startgame import GameController
    module_failed = False
except ImportError:
    module_failed = True


# In console: python -m unittest -v tests/test_pacman.py
class TestController(unittest.TestCase):
    def setUp(self):
        if module_failed:
            self.skipTest('module doesnt exist')
        self.start = GameController()
        self.start.start_game()

    def test_background(self):
        self.start.set_background()

    def test_update(self):
        self.start.update()

    def test_check_events(self):
        self.start.check_events()
        self.start.check_ghost_events()
        self.start.check_pellet_events()
        self.start.check_fruit_events()

    def test_entities(self):
        self.start.show_entities()
        self.start.hide_entities()

    def test_updatescore(self):
        self.start.update()

    def test_restart_game(self):
        self.start.restart_game()

    def test_reset_level(self):
        self.start.reset_level()

    def test_next_level(self):
        self.start.next_level()

    def test_render(self):
        self.start.render()


if __name__ == "__main__":
    unittest.main()
