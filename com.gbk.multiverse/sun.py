import pygame

import time

class Sun:
    def __init__(self, cam_width, cam_height):
        self.img = pygame.Surface((cam_width, cam_height))
        self.img.fill((0, 0, 0))  # BLACK
        self.brightness = 255
        self.rising = False
        self.period = True
        self.start_period = time.monotonic()
        self.length = 10
        self.img.set_alpha(255 - self.brightness)

    def update(self, time_):
        if self.period:
            if time.monotonic() - self.start_period > self.length:
                self.period = False

        if not self.period:
            delta = 0.4 * time_
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

            colors = {256: (255, 102, 0), 120: (26, 0, 0), 49: (0, 0, 0)}

            sorted_colors = sorted(list(colors.keys()) + [int(self.brightness)], reverse=True)
            color = sorted_colors.index(int(self.brightness))
            br_a, br_b = list(colors.keys())[color - 1], list(colors.keys())[color]
            color_a, color_b = colors[br_a], colors[br_b]
            current_color = ((int(self.brightness) - br_b) * (color_a[0] - color_b[0]) / (br_a - br_b),
                             (int(self.brightness) - br_b) * (color_a[1] - color_b[1]) / (br_a - br_b),
                             (int(self.brightness) - br_b) * (color_a[2] - color_b[2]) / (br_a - br_b))
            current_color = [int(current_color[i] + color_b[i]) for i in range(3)]
            print(current_color)
            self.img.fill(current_color)

            self.img.set_alpha(255 - self.brightness)
