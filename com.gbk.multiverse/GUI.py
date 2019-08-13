import pygame

from my_libs import Rect, Vector2D

class Bar:
    def __init__(self, length, height, width, colors):
        self.length = length
        self.height = height
        self.width = width
        self.colors = dict([(key, colors[key]) for key in sorted(colors.keys(), reverse=True)])

    def draw(self, surface, param, max_param, param_bonus, center, cam_scroll):
        scaled = param / ((max_param + param_bonus) / self.length)

        color = (0, 255, 0)
        for key in self.colors.keys():
            if scaled >= key * (self.length / 100):
                color = self.colors[key]
                break

        position = Vector2D(center.x + cam_scroll.x, center.y + cam_scroll.y)
        pygame.draw.rect(surface, color,
                         (position.x - scaled / 2, position.y - self.height / 2, scaled, self.width))