import pygame
from animation import Animation

class AnimationManager:

    def __init__(self):
        self.animations = dict()
        self.currentAnimation = ''
        self.flipped = False

    def create(self, name, filename, cols, rows, count, speed):
        self.animations[name] = Animation(filename, cols, rows, count, speed)
        self.currentAnimation = name

    def draw(self, surface, position):
        anim = self.animations[self.currentAnimation]

        if self.flipped:
            surface.blit(pygame.transform.flip(anim.sheet, True, False),
                     (position[0] + anim.center[0],
                      position[1] + anim.center[1]),
                    anim.frames[int(anim.currentFrame)])
        else:
            surface.blit(anim.sheet,
                         (position[0] + anim.center[0],
                          position[1] + anim.center[1]),
                         anim.frames[int(anim.currentFrame)])

    def set(self, name):
        self.currentAnimation = name

    def flip(self, flipped):
        self.flipped = flipped

    def tick(self, time):
        self.animations[self.currentAnimation].tick(time)

    def pause(self):
        self.animations[self.currentAnimation].isPlaying = False

    def play(self):
        self.animations[self.currentAnimation].isPlaying = True