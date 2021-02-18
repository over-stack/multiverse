import numpy as np
import random
import pygame

from object import Object
#from debug_object import DebugObject
from my_libs import Rect, Vector2D
import GUI
from genome import Genome
from copy import deepcopy

import time

COUNT_OF_BUTTONS = 323


class Entity(Object):
    def __init__(self, animanager, speed, max_health, strength, vision_area, family='single', container='entities'):
        Object.__init__(self, animanager, max_health, family, container)

        self.speed = speed
        self.acceleration = Vector2D(0, 0)
        self.strength = strength
        self.max_satiety = 100
        self.satiety = self.max_satiety
        self.satiety_speed = 0
        self.satiety_damage = 0
        self.min_satiety = 25  # min amount satiety for regeneration
        self.attack_range = Vector2D(7, 3)
        self.vision_area = vision_area

        self.speed_bonus = 0
        self.strength_bonus = 0
        self.satiety_bonus = 0
        self.satiety_speed_bonus = 0

        self.busy = False
        self.request = False  # request for action
        self.ai = True

        self.friends = list()
        self.friendly_fire = False
        self.friendly_collision = True

        self.satiety_bar = GUI.Bar(self.get_rect().width, self.get_rect().height, 2,
                                   {100: (105, 17, 17)})

        self.priorities = dict()

        self.genome_layers = [9, 30, 40, 30, 5]
        self.genome = Genome(layers=self.genome_layers)

        self.feature = None  ####################
        self.features = [0] * 9
        self.answers = list()
        self.write_features = True

        self.ai_custom = False

        #self.debug_object = DebugObject()

    def set_genome(self, genome):
        self.genome = genome.copy()

    def generate_random_priorities(self, env_states):
        nums = [random.uniform(0, 1)]
        for i in range(len(env_states) - 1):
            nums.append(random.uniform(0, 1 - sum(nums)))
        nums.append(1 - sum(nums))

        for i in range(len(env_states)):
            self.priorities[env_states[i]] = nums[i]

    def control(self, time_, entities_around, decorations_around, keys=list(), pass_=False):
        #start = time.monotonic()
        if not pass_:
            self.features = self.encode_features(entities_around, decorations_around)
        #end = time.monotonic()
        if self.ai:
            '''
                    [health,
                     self.get_direction(),
                     e_x,
                     e_y,
                     e_health,
                     e_direction,
                     d_x,
                     d_y,
                     d_health]
                     '''
            if self.ai_custom:
                '''
                buttons = []
                if True:  # health  features[0] >= features[4]
                    if self.features[1] < 0:  # direction
                        if self.features[2] < 0:  # dir to e
                            if np.abs(self.features[2]) <= 0.12:  # e_x
                                buttons.append(' ')  # attack
                            else:
                                buttons.append('a')  # left
                        else:
                            buttons.append('d')
                            if np.abs(self.features[2]) <= 0.12:  # e_x
                                buttons.append(' ')  # attack
                    else:  # direction
                        if self.features[2] > 0:  # dir to e
                            if np.abs(self.features[2]) <= 0.12:  # e_x
                                buttons.append(' ')  # attack
                            else:
                                buttons.append('d')  # left
                        else:
                            buttons.append('a')
                            if np.abs(self.features[2]) <= 0.12:  # e_x
                                buttons.append(' ')  # attack

                    if self.features[3] < 0:
                        if abs(self.features[3]) <= 0.12:
                            buttons.append(' ')
                        else:
                            buttons.append('w')
                    else:
                        if abs(self.features[3]) <= 0.12:
                            buttons.append(' ')
                        else:
                            buttons.append('s')

                keys = [0 for i in range(COUNT_OF_BUTTONS)]
                if buttons.count(' ') == 2:
                    keys[ord(' ')] = 1
                else:
                    for b in buttons:
                        if b != ' ':
                            keys[ord(b)] = 1
            '''
            else:
                x = self.genome.evaluate(self.features)
                keys = self.decode_features(x)


        objects_around = entities_around + decorations_around
        start = time.monotonic()

        if self.state != 'death':
            self.keys_pressed(keys, time_)
            self.keys_released(keys, time_)

        self.collision(objects_around, self.acceleration)

        self.interaction(objects_around)
        end = time.monotonic()


        return end-start

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
        '''
        if keys[pygame.K_KP4] and self.write_features:
            print(f'health = {self.feature[0]}')
            print(f'direction = {self.feature[1]}')
            print(f'e_x = {self.feature[2]}')
            print(f'e_y = {self.feature[3]}')
            print(f'e_health = {self.feature[4]}')
            print(f'e_direction = {self.feature[5]}')
            print(f'd_x = {self.feature[6]}')
            print(f'd_y = {self.feature[7]}')
            print(f'd_health = {self.feature[8]}')

            self.features.append(self.feature)
            self.answers.append([1, 0, 0, 0, 0])
            self.write_features = False
        if keys[pygame.K_KP6] and self.write_features:
            print(f'health = {self.feature[0]}')
            print(f'direction = {self.feature[1]}')
            print(f'e_x = {self.feature[2]}')
            print(f'e_y = {self.feature[3]}')
            print(f'e_health = {self.feature[4]}')
            print(f'e_direction = {self.feature[5]}')
            print(f'd_x = {self.feature[6]}')
            print(f'd_y = {self.feature[7]}')
            print(f'd_health = {self.feature[8]}')

            self.features.append(self.feature)
            self.answers.append([0, 1, 0, 0, 0])
            self.write_features = False
        if keys[pygame.K_KP8] and self.write_features:
            print(f'health = {self.feature[0]}')
            print(f'direction = {self.feature[1]}')
            print(f'e_x = {self.feature[2]}')
            print(f'e_y = {self.feature[3]}')
            print(f'e_health = {self.feature[4]}')
            print(f'e_direction = {self.feature[5]}')
            print(f'd_x = {self.feature[6]}')
            print(f'd_y = {self.feature[7]}')
            print(f'd_health = {self.feature[8]}')

            self.features.append(self.feature)
            self.answers.append([0, 0, 1, 0, 0])
            self.write_features = False
        if keys[pygame.K_KP2] and self.write_features:
            print(f'health = {self.feature[0]}')
            print(f'direction = {self.feature[1]}')
            print(f'e_x = {self.feature[2]}')
            print(f'e_y = {self.feature[3]}')
            print(f'e_health = {self.feature[4]}')
            print(f'e_direction = {self.feature[5]}')
            print(f'd_x = {self.feature[6]}')
            print(f'd_y = {self.feature[7]}')
            print(f'd_health = {self.feature[8]}')

            self.features.append(self.feature)
            self.answers.append([0, 0, 0, 1, 0])
            self.write_features = False
        if keys[pygame.K_KP5] and self.write_features:
            print(f'health = {self.feature[0]}')
            print(f'direction = {self.feature[1]}')
            print(f'e_x = {self.feature[2]}')
            print(f'e_y = {self.feature[3]}')
            print(f'e_health = {self.feature[4]}')
            print(f'e_direction = {self.feature[5]}')
            print(f'd_x = {self.feature[6]}')
            print(f'd_y = {self.feature[7]}')
            print(f'd_health = {self.feature[8]}')

            self.features.append(self.feature)
            self.answers.append([0, 0, 0, 0, 1])
            self.write_features = False

        if keys[pygame.K_p]:
            with open('features.txt', 'w', encoding='utf-8') as f:
                for feature in self.features:
                    f.write(' '.join(str(i) for i in feature) + '\n')
            with open('answers.txt', 'w', encoding='utf-8') as f:
                for answer in self.answers:
                    f.write(' '.join(str(i) for i in answer) + '\n')
        '''

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
        ''''
        if not keys[pygame.K_KP4] and not keys[pygame.K_KP6] and not keys[pygame.K_KP8] \
            and not keys[pygame.K_KP2] and not keys[pygame.K_KP5]:
            self.write_features = True
        '''

    def collision(self, objects, acceleration):
        '''
        allow_interaction = False
        if not self.busy or not self.request:
            if self.state == 'attack':
                if self.animanager.get_elapsed_time() >= 0.6:
                    allow_interaction = True

                    rect = self.get_rect(toDraw=False)
                    if not self.animanager.flipped:
                        area = Rect(rect.right + self.attack_range.x / 2, rect.center.y,
                                    self.attack_range.x, self.attack_range.y, isCenter=True)
                    else:
                        area = Rect(rect.left - self.attack_range.x / 2, rect.center.y,
                                    self.attack_range.x, self.attack_range.y, isCenter=True)
        '''

        collision_rect = self.get_collision_rect()
        next_collision_rect = self.get_collision_rect()
        next_collision_rect.move(acceleration.x, acceleration.y)

        if not self.isCollision:
            return

        for object_ in objects:
            if not object_.isCollision:
                continue
            if not self.friendly_collision and object_.family in self.friends:
                continue
            object_collision_rect = object_.get_collision_rect()
            if not next_collision_rect.intersects(object_collision_rect):
                continue

            next_collision_rect.move(0, -self.acceleration.y)
            if next_collision_rect.intersects(object_collision_rect):
                if acceleration.x > 0:
                    acceleration.x = object_collision_rect.left - collision_rect.right
                elif acceleration.x < 0:
                    acceleration.x = object_collision_rect.right - collision_rect.left
                collision_rect.move(acceleration.x, 0)
                next_collision_rect.move_to(collision_rect.center.x, collision_rect.center.y, isCenter=True)

            next_collision_rect.move(0, self.acceleration.y)
            if next_collision_rect.intersects(object_collision_rect):
                if acceleration.y > 0:
                    acceleration.y = object_collision_rect.top - collision_rect.bottom
                elif acceleration.y < 0:
                    acceleration.y = object_collision_rect.bottom - collision_rect.top
                collision_rect.move(0, acceleration.y)
                next_collision_rect.move_to(collision_rect.center.x, collision_rect.center.y, isCenter=True)

            '''
            if allow_interaction:
                if object_.get_rect().intersects(area):
                    if not self.friendly_fire and object_.family in self.friends:  # OFF FRIENDLY FIRE
                        continue
                    object_.health -= self.strength + self.strength_bonus
                    object_.health = max(0, object_.health)
                    if object_.container == 'entities' and not object_.immortal:
                        # self.satiety += 100  # vampire
                        self.health += (self.regeneration_speed + self.regeneration_speed_bonus)
                        self.score += 1000
            '''

        self.position += acceleration

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
                if obj.get_rect().intersects(area):
                    if not self.friendly_fire and obj.family in self.friends:  # OFF FRIENDLY FIRE
                        continue
                    obj.health -= self.strength + self.strength_bonus
                    obj.health = max(0, obj.health)
                    if obj.container == 'entities' and not obj.immortal:
                            #self.satiety += 100  # vampire
                            self.health += (self.regeneration_speed + self.regeneration_speed_bonus)
                            self.score += 1000

        self.request = False

    def update(self, time):
        Object.update(self, time)

        self.score += time  #######################

        if self.satiety > 0:
            self.satiety -= self.satiety_speed * time
        else:
            self.satiety = 0.
            self.health -= self.satiety_damage * time

        if self.satiety > self.max_satiety + self.satiety_bonus:
            self.satiety = self.max_satiety + self.satiety_bonus

        if self.satiety > self.min_satiety:
            pass
            #self.health += (self.regeneration_speed + self.regeneration_speed_bonus) * time

    def draw(self, surface, cam_frame):
        Object.draw(self, surface, cam_frame)
        if not self.visible:
            return
        self.satiety_bar.draw(surface, self.satiety, self.max_satiety, self.satiety_bonus, self.position, cam_frame)

        #self.debug_object.draw(surface, cam_frame)
        #self.debug_object.erase()

    def copy(self):
        dc = deepcopy(self)
        dc.id_ = id(dc)
        dc.genome = Genome(self.genome_layers)
        return dc

    def encode_features(self, entities_around, decorations_around):
        health = min(self.health / (self.max_health + self.health_bonus), 1)

        enemies_around = [ent for ent in entities_around if ent.family not in self.friends]
        e_x = 1
        e_y = 1
        e_health = 0
        e_direction = 1
        if len(enemies_around) > 0:
            nmin = 0
            valuemin = self.get_collision_rect().distance_polar(enemies_around[0].get_collision_rect())[1]
            for i in range(1, len(enemies_around)):
                new_value = self.get_collision_rect().distance_polar(enemies_around[i].get_collision_rect())[1]
                if new_value < valuemin:
                    nmin = i
                    valuemin = new_value
            enemy = enemies_around[nmin]
            e_x, e_y = self.get_collision_rect().distance2d(enemy.get_collision_rect())
            e_x = e_x / (self.vision_area.x / 2)
            e_y = e_y / (self.vision_area.y / 2)
            e_x = min(max(-1, e_x), 1)
            e_y = min(max(-1, e_y), 1)
            e_health = min(enemy.health / (enemy.max_health + enemy.health_bonus), 1)
            e_direction = enemy.get_direction()

        d_x = 1
        d_y = 1
        d_health = 0
        if len(decorations_around) > 0:
            nmin = 0
            valuemin = self.get_collision_rect().distance_polar(decorations_around[0].get_collision_rect())[1]
            for i in range(1, len(decorations_around)):
                new_value = self.get_collision_rect().distance_polar(decorations_around[i].get_collision_rect())[1]
                if new_value < valuemin:
                    nmin = i
                    valuemin = new_value
            decoration = decorations_around[nmin]
            d_x, d_y = self.get_collision_rect().distance2d(decoration.get_collision_rect())
            d_x = d_x / (self.vision_area.x / 2)
            d_y = d_y / (self.vision_area.y / 2)
            d_health = min(decoration.health / (decoration.max_health + decoration.health_bonus), 1)

        features = [health,
                    self.get_direction(),
                    e_x,
                    e_y,
                    e_health,
                    e_direction,
                    d_x,
                    d_y,
                    d_health]

        return features

    def decode_features(self, x):
        '''
        buttons = self.genome.evaluate(features)
        for b in buttons:
            keys[ord(b)] = 1
        '''

        button = ' '
        m = np.argmax(x)
        if m == 0:
            button = 'a'
        elif m == 1:
            button = 'd'
        elif m == 2:
            button = 'w'
        elif m == 3:
            button = 's'
        elif m == 4:
            button = ' '

        keys = [0 for i in range(COUNT_OF_BUTTONS)]
        keys[ord(button)] = 1
        return keys