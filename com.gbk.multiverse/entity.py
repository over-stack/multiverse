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
        self.busy = False

    def control(self, keys):

        self.keys_pressed(keys)
        self.keys_released(keys)

        self.animanager.set(self.state)

    def keys_pressed(self, keys):

        if keys[pygame.K_d]:
            if not self.busy:
                self.acceleration[0] = self.speed
                self.state = 'walk'

            self.animanager.flip(False)

        if keys[pygame.K_a]:
            if not self.busy:
                self.acceleration[0] = -self.speed
                self.state = 'walk'

            self.animanager.flip(True)

        if keys[pygame.K_w]:
            if not self.busy:
                self.acceleration[1] = -self.speed
                self.state = 'walk'

        if keys[pygame.K_s]:
            if not self.busy:
                self.acceleration[1] = self.speed
                self.state = 'walk'

        if keys[pygame.K_SPACE]:
            if not self.busy:
                self.state = 'attack'
                self.busy = True

    def keys_released(self, keys):

        if not (keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_SPACE]):
            if not self.busy:
                self.acceleration[0] = 0
                self.acceleration[1] = 0
                self.state = 'stay'

        if not (keys[pygame.K_SPACE]) and self.state == 'attack':
            if not self.animanager.get().isPlaying:
                self.animanager.play()
                self.state = 'stay'
                self.busy = False

    # Do after control and before update
    def check_collision(self, objects):

        if not self.collision:
            return

        left = self.position[0] - self.width / 2
        right = left + self.width
        top = self.position[1] - self.height / 2
        bottom = top + self.height

        for object in objects:

            if not object.collision or self.position == object.position: # this position like self detection
                continue

            obj_left = object.position[0] - object.width / 2
            obj_right = obj_left + object.width
            obj_top = object.position[1] - object.height / 2
            obj_bottom = obj_top + object.height

            # If we go Right
            if (right >= obj_left) and (left < obj_left):
                if (bottom > obj_top) and (top < obj_bottom): # < > not <= >= because of teleporting
                    if self.acceleration[0] > 0:
                        self.acceleration[0] = 0
                        self.position[0] = obj_left - self.width / 2

            # Left
            if (left <= obj_right) and (right > obj_right):
                if (bottom > obj_top) and (top < obj_bottom):
                    if self.acceleration[0] < 0:
                        self.acceleration[0] = 0
                        self.position[0] = obj_right + self.width / 2

            # Bottom
            if (bottom >= obj_top) and (top < obj_top):
                if (right > obj_left) and (left < obj_right):
                    if self.acceleration[1] > 0:
                        self.acceleration[1] = 0
                        self.position[1] = obj_top - self.height / 2

            # Top
            if (top <= obj_bottom) and (bottom > obj_bottom):
                if (right > obj_left) and (left < obj_right):
                    if self.acceleration[1] < 0:
                        self.acceleration[1] = 0
                        self.position[1] = obj_bottom + self.height / 2

    def update(self, time):
        Object.update(self, time)

        self.position[0] += self.acceleration[0] * time
        self.position[1] += self.acceleration[1] * time