import random
import pygame

from object import Object
from my_libs import Rect, Vector2D
import GUI
from genome import Genome
from copy import deepcopy

COUNT_OF_BUTTONS = 323


class Entity(Object):
    def __init__(self, animanager, position, speed, max_health, strength, family='single', type_='entity'):
        Object.__init__(self, animanager, position, max_health, family, type_)

        self.speed = speed
        self.acceleration = Vector2D(0, 0)
        self.strength = strength
        self.max_satiety = 100
        self.satiety = self.max_satiety
        self.satiety_speed = 0.5
        self.satiety_damage = 2
        self.min_satiety = 25  # min amount satiety for regeneration
        self.attack_range = Vector2D(7, 3)

        self.speed_bonus = 0
        self.strength_bonus = 0
        self.satiety_bonus = 0
        self.satiety_speed_bonus = 0

        self.busy = False
        self.request = False  # request for action
        self.ai = True

        self.satiety_bar = GUI.Bar(self.get_rect().width, self.get_rect().height, 2,
                                   {100: (105, 17, 17)})

        self.priorities = dict()

        self.genome = Genome()

    def set_genome(self, genome, mutation=False):
        self.genome = genome.copy()
        if mutation:
            self.genome.mutation()

    def generate_random_priorities(self, env_states):
        nums = [random.uniform(0, 1)]
        for i in range(len(env_states) - 1):
            nums.append(random.uniform(0, 1 - sum(nums)))
        nums.append(1 - sum(nums))

        for i in range(len(env_states)):
            self.priorities[env_states[i]] = nums[i]

    def ai_control(self, features, time, objects_around):
        buttons = {0: ' ', 1: 'a', 2: 'w', 3: 'd', 4: 's'}
        keys = [0 for i in range(COUNT_OF_BUTTONS)]
        result = self.genome.evaluate(features)
        for r in result:
            keys[ord(buttons[r])] = 1
        self.control(keys, time, objects_around)

    def control(self, keys, time, objects_around):
        if self.state != 'death':
            self.keys_pressed(keys, time)
            self.keys_released(keys, time)

        self.collision(objects_around, Vector2D(self.acceleration.x, 0))
        self.collision(objects_around, Vector2D(0, self.acceleration.y))

        self.interaction(objects_around)

    def keys_pressed(self, keys, time):
        if keys[pygame.K_d]:
            if not self.busy:
                self.acceleration.x = self.speed * time
                self.state = 'walk'

                self.animanager.flip(False)

        if keys[pygame.K_a]:
            if not self.busy:
                self.acceleration.x = -self.speed * time
                self.state = 'walk'

                self.animanager.flip(True)

        if keys[pygame.K_w]:
            if not self.busy:
                self.acceleration.y = -self.speed * time
                self.state = 'walk'

        if keys[pygame.K_s]:
            if not self.busy:
                self.acceleration.y = self.speed * time
                self.state = 'walk'

        if keys[pygame.K_SPACE]:
            self.acceleration.x = 0
            self.acceleration.y = 0
            if self.state == 'attack' and not self.animanager.get().isPlaying:
                self.busy = False
                self.animanager.start()

            if not self.busy:
                self.state = 'attack'
                self.busy = True
                self.request = True

    def keys_released(self, keys, time):
        if not (keys[pygame.K_d] or keys[pygame.K_a] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_SPACE]):
            if not self.busy:
                self.acceleration.x = 0
                self.acceleration.y = 0
                self.state = 'stay'

        if not keys[pygame.K_a]:
            if self.acceleration.x < 0:
                self.acceleration.x = 0

        if not keys[pygame.K_d]:
            if self.acceleration.x > 0:
                self.acceleration.x = 0

        if not keys[pygame.K_w]:
            if self.acceleration.y < 0:
                self.acceleration.y = 0

        if not keys[pygame.K_s]:
            if self.acceleration.y > 0:
                self.acceleration.y = 0

        if not (keys[pygame.K_SPACE]) and self.state == 'attack':
            if not self.animanager.get().isPlaying:
                self.animanager.play()
                self.state = 'stay'
                self.busy = False

    def collision(self, objects, acceleration):
        self.position += acceleration
        if not self.isCollision:
            return

        collision_rect = self.get_collision_rect()
        for object_ in objects:
            if not object_.isCollision or self.id_ == object_.id_:
                continue
            object_collision_rect = object_.get_collision_rect()
            if not collision_rect.intersects(object_collision_rect):
                continue

            if acceleration.x > 0:
                self.position.x += object_collision_rect.left - collision_rect.right
            elif acceleration.x < 0:
                self.position.x += object_collision_rect.right - collision_rect.left

            if acceleration.y > 0:
                self.position.y += object_collision_rect.top - collision_rect.bottom
            elif acceleration.y < 0:
                self.position.y += object_collision_rect.bottom - collision_rect.top

    def interaction(self, objects_around):
        if not (self.busy and self.request):
            return

        if self.state == 'attack':
            if self.animanager.get_elapsed_time() < 0.6:
                return
            rect = self.get_rect(toDraw=False)
            if not self.animanager.flipped:
                area = Rect(rect.right + self.attack_range.x / 2, rect.center.y,
                            self.attack_range.x, self.attack_range.y, isCenter=True)
            else:
                area = Rect(rect.left - self.attack_range.x / 2, rect.center.y,
                            self.attack_range.x, self.attack_range.y, isCenter=True)
            for obj in objects_around:
                if self.id_ != obj.id_:
                    if obj.get_rect().intersects(area):
                        obj.health -= self.strength + self.strength_bonus
                        if obj.type_ == 'entity' and obj.family != 'hero':
                            self.satiety += 50  # vampire

        self.request = False

    def update(self, time):
        Object.update(self, time)

        if self.satiety > 0:
            self.satiety -= self.satiety_speed * time
        else:
            self.satiety = 0.
            self.health -= self.satiety_damage * time

        if self.satiety > self.max_satiety + self.satiety_bonus:
            self.satiety = self.max_satiety + self.satiety_bonus

        if self.satiety > self.min_satiety:
            self.health += (self.regeneration_speed + self.regeneration_speed_bonus) * time

    def draw(self, surface, cam_frame):
        Object.draw(self, surface, cam_frame)
        if not self.visible:
            return
        self.satiety_bar.draw(surface, self.satiety, self.max_satiety, self.satiety_bonus, self.position, cam_frame)

    def copy(self):
        dc = deepcopy(self)
        dc.id_ = id(dc)
        dc.genome = Genome()
        return dc

    def get_direction(self):
        if self.animanager.flipped:
            return 'left'
        return 'right'
