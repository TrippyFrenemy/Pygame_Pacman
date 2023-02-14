import pygame
from pygame.locals import *
from constants import *


class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None

    def setBackground(self):
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackground()

    def update(self):
        self.checkEvents()
        self.render()







    def checkEvents(self):
        pass

    def render(self):
        pass