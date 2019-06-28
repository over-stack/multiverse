import random
import pygame
from object import Object

class Entity(Object):
    def __init__(self, animanager, position, speed, max_health, strength, id_, family='single', type='entity'):
        Object.__init__(self, animanager, position, id_, max_health, family, type)

        self.position = position
        self.speed = speed
        self.acceleration = [0, 0]
        self.strength = strength

        self.state = 'stay'
        self.busy = False
        self.alive = True

        self.objects_around = []

        self.request = False # request for action

        self.max_satiety = 100
        self.satiety = self.max_satiety
        self.satiety_speed = 0.05
        self.satiety_damage = 0.05
        self.min_satiety = 25  # min amount satiety for regeneration

        self.speed_bonus = 0
        self.strength_bonus = 0
        self.satiety_bonus = 0
        self.regeneration_speed_bonus = 0
        self.satiety_speed_bonus = 0

        self.attack_area_size = [40, 40]

        self.ai = True
        self.priorities = dict()

    def generate_priorities(self, env_states):

        nums = [random.uniform(0, 1)]
        for i in range(len(env_states) - 1):
            nums.append(random.uniform(0, 1 - sum(nums)))
        nums.append(1 - sum(nums))

        for i in range(len(env_states)):
            self.priorities[env_states[i]] = nums[i]

    def control(self, keys):

        if self.state != 'death':
            self.keys_pressed(keys)
            self.keys_released(keys)

    def ai_control(self, decision):

        keys = dict(zip([pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_SPACE],
                        [False, False, False, False, False]))

        if decision < 5:
            keys[list(keys.keys())[decision]] = True

        self.control(keys)

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

            if not object.collision or self.id_ == object.id_:
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

        if self.health <= 0:
            self.die()

        self.animanager.set(self.state)
        Object.update(self, time)

        self.position[0] += self.acceleration[0] * time
        self.position[1] += self.acceleration[1] * time

        if self.state == 'death':
            if not self.animanager.get().isPlaying or not self.animanager.currentAnimation == 'death':
                self.alive = False

        if self.busy and self.request:
            if self.state == 'attack':
                if self.animanager.get().currentFrame > self.animanager.get().frames_count / 2: # animation time
                    self.interact()
                    self.request = False

        if self.satiety > 0:
            self.satiety -= self.satiety_speed
        else:
            self.health -= self.satiety_damage

        if self.satiety > self.max_satiety + self.satiety_bonus:
            self.satiety = self.max_satiety + self.satiety_bonus

        if self.satiety > self.min_satiety:
            self.health += self.regeneration_speed + self.regeneration_speed_bonus

    def die(self):
        self.state = 'death'

    def look_around(self, objects_around, world_around):
        self.objects_around = objects_around

    def interact(self):
        if self.state == 'attack':

            area = [self.position[0] + self.width // 2, self.position[1] - self.height // 2] + self.attack_area_size
            if self.animanager.flipped:
                area[0] -= self.width + self.attack_area_size[0]

            for obj in self.objects_around:
                if self.id_ != obj.id_:
                    if obj.in_area(area):
                        obj.health -= self.strength + self.strength_bonus
                        self.satiety += 20  # only for debug

    def draw(self, surface, cam_frame):
        Object.draw(self, surface, cam_frame)

        position = [self.position[0] + cam_frame[0], self.position[1] + cam_frame[1]]

        satiety_line_width = 40
        scaled_satiety = self.satiety / (100 / satiety_line_width)
        pygame.draw.rect(surface, (128, 0, 0),
                         (position[0] - scaled_satiety / 2, position[1] - self.height / 2 + 4, scaled_satiety, 2))

    def get_features(self):

        my = [self.health, self.satiety, self.strength, self.speed]

        if not len(self.objects_around):
            features = my + [0] * 8
            return features

        # min_health = entities[min(enumerate(ent_health), key=itemgetter(1))[0]]
        features = my + [0] * 8

        return features

    def sex(self, entity, free_id):
        if entity.family == self.family:
            return Entity(self.animanager.copy(), self.position, self.speed, self.max_health,
                          self.strength, free_id, family=self.family)
