import pygame
from object import Object

class Entity(Object):

    def __init__(self, animanager, position, speed, max_health, strength, id):
        Object.__init__(self, animanager, position, id, max_health)

        self.position = position
        self.speed = speed
        self.acceleration = [0, 0]
        self.strength = strength

        self.state = 'stay'
        self.busy = False
        self.alive = True

        self.objects_around = []

        self.have_not_death_anim = False # only for debugging
        self.request = False # request for action

    def control(self, keys):

        if self.state != 'death':
            self.keys_pressed(keys)
            self.keys_released(keys)

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
            self.acceleration[0] = 0
            self.acceleration[1] = 0
            if self.state == 'attack' and not self.animanager.get().isPlaying:
                self.busy = False
                self.animanager.start()
            if not self.busy:
                self.state = 'attack'
                self.busy = True
                self.request = True

    def keys_released(self, keys):

        if not (keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_SPACE]):
            if not self.busy:
                self.acceleration[0] = 0
                self.acceleration[1] = 0
                self.state = 'stay'

        if not keys[pygame.K_a]:
            if self.acceleration[0] < 0:
                self.acceleration[0] = 0

        if not keys[pygame.K_d]:
            if self.acceleration[0] > 0:
                self.acceleration[0] = 0

        if not keys[pygame.K_w]:
            if self.acceleration[1] < 0:
                self.acceleration[1] = 0

        if not keys[pygame.K_s]:
            if self.acceleration[1] > 0:
                self.acceleration[1] = 0

        if not (keys[pygame.K_SPACE]) and self.state == 'attack':
            if not self.animanager.get().isPlaying:
                self.animanager.play()
                self.state = 'stay'
                self.busy = False

    # Do after control and before update
    def check_collision(self, objects):

        if not self.collision:
            return

        left = self.position[0] - self.width / 2 + (self.width / 8) # + shift
        right = left + self.width - (self.width / 4) # - shift
        top = self.position[1] - self.height / 2 + self.depth
        bottom = top + self.height / 2

        width = right - left
        height = bottom - top

        for object in objects:

            if not object.collision or self.id == object.id:
                continue

            obj_left = object.position[0] - object.width / 2 + (object.width / 8) # + shift
            obj_right = obj_left + object.width - (object.width / 4) # - shift
            obj_top = object.position[1] - object.height / 2 + object.depth
            obj_bottom = obj_top + object.height / 2

            # If we go Right
            if (right >= obj_left) and (left <= obj_left): # <= => not < > because of angles
                if (bottom > obj_top) and (top < obj_bottom): # < > not <= >= because of teleporting
                    if self.acceleration[0] > 0:
                        self.acceleration[0] = 0
                        self.position[0] = obj_left - width / 2

            # Left
            if (left <= obj_right) and (right >= obj_right):
                if (bottom > obj_top) and (top < obj_bottom):
                    if self.acceleration[0] < 0:
                        self.acceleration[0] = 0
                        self.position[0] = obj_right + width / 2

            # Bottom
            if (bottom >= obj_top) and (top <= obj_top):
                if (right > obj_left) and (left < obj_right):
                    if self.acceleration[1] > 0:
                        self.acceleration[1] = 0
                        self.position[1] = obj_top - (height + self.depth) / 2

            # Top
            if (top <= obj_bottom) and (bottom >= obj_bottom):
                if (right > obj_left) and (left < obj_right):
                    if self.acceleration[1] < 0:
                        self.acceleration[1] = 0
                        self.position[1] = obj_bottom + (height + self.depth) / 2 - self.depth

    def update(self, time):
        self.animanager.set(self.state)
        Object.update(self, time)

        self.position[0] += self.acceleration[0] * time
        self.position[1] += self.acceleration[1] * time

        if self.state == 'death' and not self.animanager.get().isPlaying:
            self.alive = False

        if self.busy and self.request:
            if self.state == 'attack':
                if self.animanager.get().currentFrame > self.animanager.get().frames_count / 2: # animation time
                    self.interact()
                    self.request = False

    def die(self):
        if self.have_not_death_anim: # change it
            self.alive = False
        else:
            self.state = 'death'

    def vision(self, objects):
        self.objects_around = objects

    def interact(self):
        if self.state == 'attack':

            area = [self.position[0] + self.width // 2, self.position[1] - self.height // 2, 40, 40]
            if self.animanager.flipped:
                area[0] -= self.width + 40

            for obj in self.objects_around:
                if self.id != obj.id:
                    if obj.in_area(area):
                        obj.health -= self.strength