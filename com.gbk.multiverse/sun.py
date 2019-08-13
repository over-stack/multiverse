import pygame

class Sun:
    def __init__(self, cam_width, cam_height):
        self.img = pygame.Surface((cam_width, cam_height))
        self.img.fill((0, 0, 0))
        self.brightness = 255

    def update(self, time):
        self.brightness -= 0.1 * time
        self.img.set_alpha(255 - self.brightness)