import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint


class Entity(object):
    def __init__(self, node):
        self.name = None
        self.directions = {UP: Vector2(0, -1), DOWN: Vector2(0, 1),
                           LEFT: Vector2(-1, 0), RIGHT: Vector2(1, 0), STOP: Vector2()}
        self.direction = STOP
        self.setSpeed(100)
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.node = node
        self.setPosition()
        self.target = node
        self.visible = True
        self.disablePortal = False

    def setPosition(self):
        self.position = self.node.position.copy()

    def validDirection(self, direction):
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
        return False

    def getNewTarget(self, direction):
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

    def overshotTarget(self):
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared()
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False

    def reverseDirection(self):
        self.direction *= -1
        temp = self.node
        self.node = self.target
        self.target = temp

    def oppositeDirection(self, direction):
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def setSpeed(self, speed):
        self.speed = speed * TILEWIDTH / 16

    def render(self, screen):
        if self.visible:
            p = self.position.asInt()
            pygame.draw.circle(screen, self.color, p, self.radius)

