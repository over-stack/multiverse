from copy import deepcopy
from pygame import transform
from animation import Animation

from my_libs import Rect, Vector2D


class AnimationManager:
    def __init__(self, defaultFlipped=False):
        self.animations = dict()
        self.currentAnimation = ''
        self.lastAnimation = ''
        self.flipped = False
        self.defaultFlipped = defaultFlipped

    def create(self, name, sheet, cols, rows, count, speed, looped=False):
        self.animations[name] = Animation(sheet, cols, rows, count, speed, looped)
        self.currentAnimation = name

    def draw(self, surface, topleft, cam_scroll):  # position = topleft
        position = Vector2D(topleft.x + cam_scroll.x,
                            topleft.y + cam_scroll.y)

        anim = self.animations[self.currentAnimation]
        flipped = self.flipped
        if self.defaultFlipped:
            flipped = not self.flipped
        if flipped:
            surface.blit(transform.flip(anim.sheet, True, False),
                         (position.x, position.y),
                         anim.frames[min(int(anim.currentFrame), anim.count - 1)].get_tuple())
        else:
            surface.blit(anim.sheet,
                         (position.x, position.y),
                         anim.frames[min(int(anim.currentFrame), anim.count - 1)].get_tuple())

    def set(self, name):
        if name not in self.animations.keys():
            name = 'stay'
        self.currentAnimation = name
        if self.lastAnimation != self.currentAnimation and len(self.lastAnimation):
            self.animations[self.lastAnimation].currentFrame = 0
        self.lastAnimation = self.currentAnimation

    def get(self, name=''):  # name = '' --> current animation
        if len(name) == 0 or name not in self.animations.keys():
            return self.animations[self.currentAnimation]
        return self.animations[name]

    def flip(self, flipped):
        self.flipped = flipped

    def tick(self, time):
        self.animations[self.currentAnimation].tick(time)

    def pause(self):
        self.animations[self.currentAnimation].isPlaying = False

    def play(self):
        self.animations[self.currentAnimation].isPlaying = True

    def start(self):
        self.animations[self.currentAnimation].currentFrame = 0
        self.play()

    def get_elapsed_time(self):
        return ((self.get().currentFrame + 1) / (self.get().count / 100)) / 100  # 0 - 1

    def copy(self):
        return deepcopy(self)