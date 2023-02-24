import pytest
from startgame import *


# In console: python -s -m pytest test_build_and_run/
@pytest.fixture
def set_up():
    start = GameController()
    start.startGame()
    return start


def test_background(set_up):
    set_up.setBackground()


def test_update(set_up):
    set_up.update()


def test_checkEvents(set_up):
    set_up.checkEvents()
    set_up.checkGhostEvents()
    set_up.checkPelletEvents()
    set_up.checkFruitEvents()


def test_entities(set_up):
    set_up.showEntities()
    set_up.hideEntities()


def test_updatescore(set_up):
    set_up.update()


def test_restartgame(set_up):
    set_up.restartGame()


def test_resetLevel(set_up):
    set_up.resetLevel()


def test_nextLevel(set_up):
    set_up.nextLevel()


def test_render(set_up):
    set_up.render()
