import pygame
from pygame import QUIT, KEYDOWN, K_SPACE
import os
from src.data.constants import SCREENSIZE, READYTXT, BLACK, RIGHT, LEFT, WHITE, PAUSETXT, SCREENHEIGHT, SCREENWIDTH, POWERPELLET
from src.data.constants import FREIGHT, SPAWN, GAMEOVERTXT
from src.fruit import Fruit
from src.ghosts import GhostGroup
from src.mazedata import MazeData
from src.nodes import NodeGroup
from src.pacman import Pacman
from src.pauser import Pause
from src.pellets import PelletGroup
from src.sprites import LifeSprites
from src.sprites import MazeSprites
from src.text import TextGroup


class GameController(object):
    def __init__(self):
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.level = 0
        self.lives = 5
        self.score = 0
        self.pause = Pause(True)
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flash_bg = False
        self.flash_time = 0.2
        self.flash_timer = 0
        self.fruit_captured = []
        self.fruitNode = None
        self.mazedata = MazeData()

    def restart_game(self):
        self.lives = 5
        self.level = 0
        self.score = 0
        self.pause.paused = True
        self.fruit = None
        self.start_game()
        self.textgroup.update_score(self.score)
        self.textgroup.update_level(self.level)
        self.textgroup.show_text(READYTXT)
        self.lifesprites.reset_lives(self.lives)
        self.fruit_captured = []

    def reset_level(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.show_text(READYTXT)

    def next_level(self):
        self.show_entities()
        self.level += 1
        self.pause.paused = True
        self.start_game()
        self.textgroup.update_level(self.level)

    def set_background(self):
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        self.background_norm = self.mazesprites.construct_background(self.background_norm, self.level % 5)
        self.background_flash = self.mazesprites.construct_background(self.background_flash, 5)
        self.flash_bg = False
        self.background = self.background_norm

    def start_game(self):
        self.mazedata.load_maze(self.level)
        self.mazesprites = MazeSprites(self.mazedata.obj.name + ".txt", self.mazedata.obj.name + "_rotation.txt")
        self.set_background()
        self.nodes = NodeGroup(self.mazedata.obj.name + ".txt")
        self.mazedata.obj.set_portal_pairs(self.nodes)
        self.mazedata.obj.connect_home_nodes(self.nodes)
        self.pacman = Pacman(self.nodes.get_node_from_tiles(*self.mazedata.obj.pacman_start))
        self.pellets = PelletGroup(self.mazedata.obj.name + ".txt")

        self.ghosts = GhostGroup(self.nodes.get_start_temp_node(), self.pacman)
        self.ghosts.pinky.set_start_node(self.nodes.get_node_from_tiles(*self.mazedata.obj.add_offset(2, 3)))
        self.ghosts.inky.set_start_node(self.nodes.get_node_from_tiles(*self.mazedata.obj.add_offset(0, 3)))
        self.ghosts.clyde.set_start_node(self.nodes.get_node_from_tiles(*self.mazedata.obj.add_offset(4, 3)))
        self.ghosts.set_spawn_node(self.nodes.get_node_from_tiles(*self.mazedata.obj.add_offset(2, 3)))
        self.ghosts.blinky.set_start_node(self.nodes.get_node_from_tiles(*self.mazedata.obj.add_offset(2, 0)))
        self.nodes.deny_home_access(self.pacman)
        self.nodes.deny_home_access_list(self.ghosts)
        self.ghosts.inky.startNode.deny_access(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.deny_access(LEFT, self.ghosts.clyde)
        self.mazedata.obj.deny_ghosts_access(self.ghosts, self.nodes)

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        self.textgroup.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.check_pellet_events()
            self.check_ghost_events()
            self.check_fruit_events()

        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)

        if self.flash_bg:
            self.flash_timer += dt
            if self.flash_timer >= self.flash_time:
                self.flash_timer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        after_pause_method = self.pause.update(dt)
        if after_pause_method is not None:
            after_pause_method()
        self.check_events()
        self.render()

    def check_fruit_events(self):
        if self.pellets.num_eaten == 50 or self.pellets.num_eaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.get_node_from_tiles(9, 20), self.level)
        if self.fruit is not None:
            if self.pacman.collide_check(self.fruit):
                self.update_score(self.fruit.points)
                self.textgroup.add_text(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8,
                                        time=1)
                fruit_captured = False
                for fruit in self.fruit_captured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruit_captured = True
                        break
                if not fruit_captured:
                    self.fruit_captured.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def check_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.set_pause(player_paused=True)
                        if not self.pause.paused:
                            self.textgroup.hide_text()
                            self.show_entities()
                        else:
                            self.textgroup.show_text(PAUSETXT)
                            self.hide_entities()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.pellets.render(self.screen)
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)

        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))

        for i in range(len(self.fruit_captured)):
            x = SCREENWIDTH - self.fruit_captured[i].get_width() * (i + 1)
            y = SCREENHEIGHT - self.fruit_captured[i].get_height()
            self.screen.blit(self.fruit_captured[i], (x, y))

        pygame.display.update()

    def check_pellet_events(self):
        pellet = self.pacman.eat_pellets(self.pellets.pelletList)
        if pellet:
            self.pellets.num_eaten += 1
            self.update_score(pellet.points)
            if self.pellets.num_eaten == 30:
                self.ghosts.inky.startNode.allow_access(RIGHT, self.ghosts.inky)
            if self.pellets.num_eaten == 70:
                self.ghosts.clyde.startNode.allow_access(LEFT, self.ghosts.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.start_freight()
            if self.pellets.is_empty():
                self.flash_bg = True
                self.hide_entities()
                self.pause.set_pause(pause_time=3, func=self.next_level)

    def check_ghost_events(self):
        for ghost in self.ghosts:
            if self.pacman.collide_ghost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.update_score(ghost.points)
                    self.textgroup.add_text(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.update_points()
                    self.pause.set_pause(pause_time=1, func=self.show_entities)
                    ghost.start_spawn()
                    self.nodes.allow_home_access(ghost)
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -= 1
                        self.lifesprites.remove_image()
                        self.pacman.die()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.textgroup.show_text(GAMEOVERTXT)
                            self.pause.set_pause(pause_time=3, func=self.restart_game)
                        else:
                            self.pause.set_pause(pause_time=3, func=self.reset_level)

    def show_entities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hide_entities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def update_score(self, points):
        self.score += points
        self.textgroup.update_score(self.score)


if __name__ == "__main__":
    game = GameController()
    game.start_game()
    while True:
        game.update()
