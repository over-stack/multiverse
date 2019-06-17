import pygame
from animationManager import AnimationManager

class Object:

    def __init__(self, animanager, position):
        self.animanager = animanager
        self.position = position
        self.collision = True

        self.width = list(self.animanager.animations.values())[0].width
        self.height = list(self.animanager.animations.values())[0].height

    def update(self, time):
        self.animanager.tick(time)

    def draw(self, surface):
        self.animanager(surface, self.position[0], self.position[1])