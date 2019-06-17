import pygame
from object import Object

class Entity(Object):

    def __init__(self, animanager, position, speed, health, strength):
        Object.__init__(self, animanager, position)

        self.position = position
        self.speed = speed
        self.acceleration = [0, 0]
        self.health = health
        self.strength = strength

        self.state = 'stay'

    def control(self, keys):
        if keys[pygame.K_d]:
            self.acceleration[0] = self.speed
            if self.state == 'stay':
                self.state = 'walk'

            self.animanager.flip(False)

        if keys[pygame.K_a]:
            self.acceleration[0] = -self.speed
            if self.state == 'stay':
                self.state = 'walk'

            self.animanager.flip(True)

        if keys[pygame.K_w]:
            self.acceleration[1] = -self.speed
            if self.state == 'stay':
                self.state = 'walk'

        if keys[pygame.K_s]:
            self.acceleration[1] = self.speed
            if self.state == 'stay':
                self.state = 'walk'

        if not (keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s]):
            self.acceleration[0] = 0
            self.acceleration[1] = 0
            if self.state == 'walk':
                self.state = 'stay'

    def update(self, time):
        Object.update(self, time)

        self.position[0] += self.acceleration[0] * time
        self.position[1] += self.acceleration[1] * time

    def draw(self, surface):
        self.animanager.draw(surface, self.position)