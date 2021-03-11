from copy import deepcopy

import pygame

from animationManager import AnimationManager
from my_libs import Rect, Vector2D
import GUI

'''
class DebugObject:
    def __int__(self, delta_position, delta_size, color):
        self.delta_position = delta_position
        self.delta_size = delta_size
        self.color = color

    def draw(self, surface, rect, cam_scroll):
        position = [rect.left + self.delta_position.x + cam_scroll.x,
                    rect.top + self.delta_position.y + cam_scroll.y]
        size = [rect.width + self.delta_size.x, rect.height + self.delta_size.y]

        pygame.draw.rect(surface, self.color, position + size)
'''


class Object:
    def __init__(self, animanager, max_health, family='single', container=None):
        self.animanager = animanager.copy()
        self.position = Vector2D(0, 0)  # center

        self.max_health = max_health
        self.health = max_health
        self.regeneration_speed = 40  # 0.7

        self.health_bonus = 0.
        self.regeneration_speed_bonus = 0.

        self.id_ = id(self)
        self.container = container
        self.family = family
        self.isCollision = True
        self.state = 'stay'
        self.alive = True
        self.visible = True
        self.immortal = False
        self.draw_bars = True

        self.score = 1

        self.animanager.set(self.state)
        self.health_bar = GUI.Bar(self.get_rect().width, self.get_rect().height + 8, 2,
                                  {100: (0, 255, 0), 75: (255, 255, 0), 25: (255, 0, 0)})

    def update(self, time):
        if self.immortal:
            self.health = self.max_health + self.health_bonus
        if self.health > self.max_health + self.health_bonus:
            self.health = self.max_health + self.health_bonus
        if self.health <= 0:
            self.health = 0.
            self.state = 'death'

        self.animanager.set(self.state)
        self.animanager.tick(time)

        if self.state == 'death':
            if not self.animanager.get().isPlaying or not self.animanager.currentAnimation == 'death':
                self.alive = False

    def draw(self, surface, cam_scroll):
        if not self.visible:
            return

        rect = self.get_collision_rect()
        pygame.draw.rect(surface, (0, 255, 0),
                         (rect.left + cam_scroll.x, rect.top + cam_scroll.y, rect.width, rect.height))
        self.animanager.draw(surface, self.get_rect().topleft, cam_scroll)

        if self.draw_bars:
            self.health_bar.draw(surface, self.health, self.max_health, self.health_bonus,
                                 self.get_rect().center, cam_scroll)

    def get_rect(self, toDraw=True): #get_draw_rect
        #if toDraw:
        #    animation = self.animanager.get()
        #else:
        #    animation = self.animanager.get('stay')
        animation = self.animanager.get()
        return Rect(self.position.x, self.position.y, animation.width, animation.height, isCenter=True)

    def get_collision_rect(self):
        #animation = self.animanager.get(name='stay')
        #return Rect(self.position.x + animation.shift, self.position.y - animation.depth,
                    #animation.width - 2 * animation.shift, animation.depth, isCenter=True)
        rect = self.animanager.get_collision_rect()
        rect.move_to(self.position.x, self.position.y, isCenter=True)
        return rect

    def copy(self):
        dc = deepcopy(self)
        dc.id_ = id(dc)
        return dc

    def get_direction(self):
        return 2 * int(not self.animanager.flipped) - 1
