import pygame

import time
import numpy as np
from genome import Genome

class Sun:
    def __init__(self, cam_width, cam_height):
        self.img = pygame.Surface((cam_width, cam_height))
        self.img.fill((0, 0, 0))  # BLACK
        self.brightness = 255
        self.img.set_alpha(255 - self.brightness)
        self.colors = {256: (255, 102, 0), 120: (26, 0, 0), 49: (0, 0, 0)}
        self.period_length = 120
        self.rising = False
        self.period = True
        self.start_period = time.monotonic()

    def update(self, time_):
        if self.period:
            if time.monotonic() - self.start_period > self.period_length:
                self.period = False

        if not self.period:
            delta = 0.1 * time_
            if not self.rising:
                if self.brightness <= 50:
                    self.brightness = 50
                    self.period = True
                    self.rising = True
            else:
                if self.brightness >= 255:
                    self.brightness = 255
                    self.period = True
                    self.rising = False
            if self.period:
                self.start_period = time.monotonic()
            self.brightness += delta * (-1) ** (not self.rising)

            sorted_colors = sorted(list(self.colors.keys()) + [self.brightness], reverse=True)
            br_index = sorted_colors.index(self.brightness)
            br_up, br_down = list(self.colors.keys())[br_index - 1], list(self.colors.keys())[br_index]
            color_up, color_down = self.colors[br_up], self.colors[br_down]
            coefficient = (self.brightness - br_down) / (br_up - br_down)
            current_color = [int(coefficient * (color_up[i] - color_down[i]) + color_down[i]) for i in range(3)]
            self.img.fill(current_color)

            self.img.set_alpha(255 - self.brightness)


if __name__ == '__main__':
    g = Genome([4, 10, 20, 10, 5])
    g.load('0.npy')
    #for layer in g.network:
        #print(layer.size)
        #print(layer)
    print(g.network)