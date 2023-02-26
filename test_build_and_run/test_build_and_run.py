import pytest
from src.startgame import GameController


# In console: python -m pytest -s -v --html=reports/report_pytest.html test_build_and_run/
@pytest.fixture
def set_up():
    start = GameController()
    start.start_game()
    return start


def test_background(set_up):
    set_up.set_background()


def test_update(set_up):
    set_up.update()


def test_check_events(set_up):
    set_up.check_events()
    set_up.check_ghost_events()
    set_up.check_pellet_events()
    set_up.check_fruit_events()


def test_entities(set_up):
    set_up.show_entities()
    set_up.hide_entities()


def test_update_score(set_up):
    set_up.update()


def test_restart_game(set_up):
    set_up.restart_game()


def test_reset_level(set_up):
    set_up.reset_level()


def test_next_level(set_up):
    set_up.next_level()


def test_render(set_up):
    set_up.render()
