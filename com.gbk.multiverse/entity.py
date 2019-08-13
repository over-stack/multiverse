import random
import pygame
from object import Object

from my_libs import Rect, Vector2D
import GUI

class Entity(Object):
    def __init__(self, animanager, position, speed, max_health, strength, id_, family='single', type_='entity'):
        Object.__init__(self, animanager, position, id_, max_health, family, type_)

        self.speed = speed
        self.acceleration = Vector2D(0, 0)
        self.strength = strength
        self.max_satiety = 100
        self.satiety = self.max_satiety
        self.satiety_speed = 0.05
        self.satiety_damage = 0.05
        self.min_satiety = 25  # min amount satiety for regeneration
        self.attack_area_size = Vector2D(40, 40)

        self.speed_bonus = 0
        self.strength_bonus = 0
        self.satiety_bonus = 0
        self.satiety_speed_bonus = 0

        self.busy = False
        self.request = False  # request for action
        self.ai = True

        self.satiety_bar = GUI.Bar(self.get_rect().width, self.get_rect().height, 2,
                                   {75: (0, 0, 255), 25: (0, 255, 255), 0: (100, 100, 50)})

        self.priorities = dict()

    def generate_random_priorities(self, env_states):
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

    def keys_pressed(self, keys):
        if keys[pygame.K_d]:
            if not self.busy:
                self.acceleration.x = self.speed
                self.state = 'walk'

                self.animanager.flip(False)

        if keys[pygame.K_a]:
            if not self.busy:
                self.acceleration.x = -self.speed
                self.state = 'walk'

                self.animanager.flip(True)

        if keys[pygame.K_w]:
            if not self.busy:
                self.acceleration.y = -self.speed
                self.state = 'walk'

        if keys[pygame.K_s]:
            if not self.busy:
                self.acceleration.y = self.speed
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

    def keys_released(self, keys):
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

    # Do after control and before update
    def collision(self, objects):
        if not self.collision:
            return

        collision_rect = self.get_collision_rect()
        for object in objects:
            if not object.isCollision or self.id_ == object.id_:
                continue
            object_collision_rect = object.get_collision_rect()
            moving = Vector2D(0, 0)

            # If we go Right
            if (collision_rect.right >= object_collision_rect.left) and \
                    (collision_rect.left <= object_collision_rect.left):  # <= => not < > because of angles
                if (collision_rect.bottom > object_collision_rect.top) and \
                        (collision_rect.top < object_collision_rect.bottom):  # < > not <= >= because of teleporting
                    if self.acceleration.x > 0:
                        self.acceleration.x = 0
                        moving.x = object_collision_rect.left - collision_rect.right

            # Left
            if (collision_rect.left <= object_collision_rect.right) and \
                    (collision_rect.right >= object_collision_rect.right):
                if (collision_rect.bottom > object_collision_rect.top) and \
                        (collision_rect.top < object_collision_rect.bottom):
                    if self.acceleration.x < 0:
                        self.acceleration.x = 0
                        moving.x = object_collision_rect.right - collision_rect.left

            # Bottom
            if (collision_rect.bottom >= object_collision_rect.top) and \
                    (collision_rect.top <= object_collision_rect.top):
                if (collision_rect.right > object_collision_rect.left) and \
                        (collision_rect.left < object_collision_rect.right):
                    if self.acceleration.y > 0:
                        self.acceleration.y = 0
                        moving.y = object_collision_rect.top - collision_rect.bottom

            # Top
            if (collision_rect.top <= object_collision_rect.bottom) and \
                    (collision_rect.bottom >= object_collision_rect.bottom):
                if (collision_rect.right > object_collision_rect.left) and \
                        (collision_rect.left < object_collision_rect.right):
                    if self.acceleration.y < 0:
                        self.acceleration.y = 0
                        moving.y = object_collision_rect.bottom - collision_rect.top

            self.position += moving

    def update(self, time):
        Object.update(self, time)

        self.position.x += self.acceleration.x * time
        self.position.y += self.acceleration.y * time

        if self.satiety > 0:
            self.satiety -= self.satiety_speed
        else:
            self.satiety = 0.
            self.health -= self.satiety_damage

        if self.satiety > self.max_satiety + self.satiety_bonus:
            self.satiety = self.max_satiety + self.satiety_bonus

        if self.satiety > self.min_satiety:
            self.health += self.regeneration_speed + self.regeneration_speed_bonus

    def interaction(self, objects_around):
        if not (self.busy and self.request):
            return

        if self.state == 'attack':
            if self.animanager.get_elapsed_time() < 0.6:
                return
            area = Rect(self.get_rect().left + self.get_rect().width, self.get_rect().top,
                        self.attack_area_size.x, self.attack_area_size.y)
            if self.animanager.flipped:
                area.left -= self.get_rect().width + self.attack_area_size.x

            for obj in objects_around:
                if self.id_ != obj.id_:
                    if obj.get_rect().intersects(area):
                        obj.health -= self.strength + self.strength_bonus
                        if obj.type_ == 'entity':
                            self.satiety += 20  # vampire

        self.request = False

    def draw(self, surface, cam_frame):
        Object.draw(self, surface, cam_frame)
        self.satiety_bar.draw(surface, self.satiety, self.max_satiety, self.satiety_bonus, self.position, cam_frame)