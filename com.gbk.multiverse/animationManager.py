from pygame import transform
from animation import Animation

class AnimationManager:

    def __init__(self):
        self.animations = dict()
        self.currentAnimation = ''
        self.lastAnimation = ''
        self.flipped = False

    def create(self, name, filename, cols, rows, count, speed, looped=False):
        self.animations[name] = Animation(filename, cols, rows, count, speed, looped)
        self.currentAnimation = name

    def draw(self, surface, position):
        anim = self.animations[self.currentAnimation]

        if self.flipped:
            surface.blit(transform.flip(anim.sheet, True, False),
                     (position[0] - anim.center[0],
                      position[1] - anim.center[1]),
                    anim.frames[int(anim.currentFrame)])
        else:
            surface.blit(anim.sheet,
                         (position[0] - anim.center[0],
                          position[1] - anim.center[1]),
                         anim.frames[int(anim.currentFrame)])

    def set(self, name):
        self.currentAnimation = name
        if self.lastAnimation != self.currentAnimation and len(self.lastAnimation):
            self.animations[self.lastAnimation].currentFrame = 0
        self.lastAnimation = self.currentAnimation

    def get(self):
        return self.animations[self.currentAnimation]

    def flip(self, flipped):
        self.flipped = flipped

    def tick(self, time):
        self.animations[self.currentAnimation].tick(time)

        if self.get().looped and not self.get().isPlaying:
            self.animations[self.currentAnimation].isPlaying = True

    def pause(self):
        self.animations[self.currentAnimation].isPlaying = False

    def play(self):
        self.animations[self.currentAnimation].isPlaying = True