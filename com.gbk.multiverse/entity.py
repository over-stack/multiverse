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

        ######## PRESSED #########

        if keys[pygame.K_d]:
            self.acceleration[0] = self.speed
            if self.state == 'stay':
                self.state = 'walk'

            self.animanager.flip(False)

        if keys[pygame.K_a]:
            self.acceleration[0] = -self.speed
            self.state = 'walk'

            self.animanager.flip(True)

        if keys[pygame.K_w]:
            self.acceleration[1] = -self.speed
            self.state = 'walk'

        if keys[pygame.K_s]:
            self.acceleration[1] = self.speed
            self.state = 'walk'

        if keys[pygame.K_SPACE]:
            self.state = 'attack'

        ######## RELEASED ##########

        if not (keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_SPACE]):
            self.acceleration[0] = 0
            self.acceleration[1] = 0
            self.state = 'stay'

        self.animanager.set(self.state)

    # Do after control and before update
    def check_collision(self, objects):

        if not self.collision:
            return

        rect = pygame.Rect(self.position[0] - self.width / 2, self.position[1] - self.height / 2,
                           self.width, self.height)

        for object in objects:

            if not object.collision:
                continue

            obj_rect = pygame.Rect(object.position[0] - object.width / 2, object.position[1] - object.height / 2,
                                   object.width, object.height)

            # If we go Right
            if (rect.right >= obj_rect.left) and (rect.left < obj_rect.left):
                if (rect.bottom > obj_rect.top) and (rect.top < obj_rect.bottom): # < > not <= >= because of teleporting
                    if self.acceleration[0] > 0:
                        self.acceleration[0] = 0
                        self.position[0] = obj_rect.left - rect.width / 2

            # Left
            if (rect.left <= obj_rect.right) and (rect.right > obj_rect.right):
                if (rect.bottom > obj_rect.top) and (rect.top < obj_rect.bottom):
                    if self.acceleration[0] < 0:
                        self.acceleration[0] = 0
                        self.position[0] = obj_rect.right + rect.width / 2

            # Bottom
            if (rect.bottom >= obj_rect.top) and (rect.top < obj_rect.top):
                if (rect.right > obj_rect.left) and (rect.left < obj_rect.right):
                    if self.acceleration[1] > 0:
                        self.acceleration[1] = 0
                        self.position[1] = obj_rect.top - rect.height / 2

            # Top
            if (rect.top <= obj_rect.bottom) and (rect.bottom > obj_rect.bottom):
                if (rect.right > obj_rect.left) and (rect.left < obj_rect.right):
                    if self.acceleration[1] < 0:
                        self.acceleration[1] = 0
                        self.position[1] = obj_rect.bottom + rect.height / 2

    def update(self, time):
        Object.update(self, time)

        self.position[0] += self.acceleration[0] * time
        self.position[1] += self.acceleration[1] * time