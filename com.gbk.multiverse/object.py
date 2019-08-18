from copy import deepcopy

import pygame

from animationManager import AnimationManager
from my_libs import Rect, Vector2D
import GUI


class Object:
    def __init__(self, animanager, position, id_, max_health=100, family='single', type_='object'):
        self.animanager = animanager
        self.position = position  # center

        self.max_health = max_health
        self.health = max_health
        self.regeneration_speed = 0.1

        self.health_bonus = 0.
        self.regeneration_speed_bonus = 0.

        self.id_ = id_
        self.type_ = type_
        self.family = family
        self.isCollision = True
        self.state = 'stay'
        self.alive = True

        self.animanager.set(self.state)
        self.health_bar = GUI.Bar(self.get_rect().width, self.get_rect().height + 8, 2,
                                  {75: (0, 255, 0), 25: (255, 0, 0), 0: (0, 0, 0)})

    def update(self, time):
        if self.health <= 0:
            self.state = 'death'

        self.animanager.set(self.state)
        self.animanager.tick(time)

        if self.state == 'death':
            if not self.animanager.get().isPlaying or not self.animanager.currentAnimation == 'death':
                self.alive = False

        if self.health > self.max_health + self.health_bonus:
            self.health = self.max_health + self.health_bonus
        if self.health < 0:
            self.health = 0.

    def draw(self, surface, cam_scroll):
        self.animanager.draw(surface, self.get_rect().topleft, cam_scroll)
        self.health_bar.draw(surface, self.health, self.max_health, self.health_bonus,
                             self.get_rect().center, cam_scroll)

    def get_rect(self, name=''):
        animation = self.animanager.get(name)
        return Rect(self.position.x, self.position.y, animation.width, animation.height, isCenter=True)

    def get_collision_rect(self):
        rect = self.get_rect('stay')
        animation = self.animanager.get(name='stay')
        return Rect(rect.left + animation.shift, rect.bottom - animation.depth,
                    rect.width - 2 * animation.shift, animation.depth)

    def copy(self):
        return deepcopy(self)
