from pygame import image, Rect
import pygame

from my_libs import Rect, Vector2D

class World:

    def __init__(self, filename, size, tile_size):
        self.image = image.load(filename)
        self.size = size
        self.size_in_tiles = Vector2D(size.x // tile_size.x, size.y // tile_size.y)
        self.tile_size = tile_size
        self.matrix = self.generate_matrix()
        self.tiles = dict()

        self.heat_map = list()
        self.rain_map = list()
        self.water_map = list()

    def generate_world(self):
        pass

    def get_world_around(self, position):
        return self.heat_map

    def add_tile(self, position, code):
        self.tiles[code] = position

    def generate_matrix(self):
        return [[0 for _ in range(self.size_in_tiles.x)] for _ in range(self.size_in_tiles.y)]

    def draw(self, surface, scroll, position, width, height):

        left = int((position.x - width) // self.tile_size.x)
        right = int((position.x + width) // self.tile_size.x)
        top = int((position.y - height) // self.tile_size.y)
        bottom = int((position.y + height) // self.tile_size.y)

        if left < 0:
            left = 0

        if right < 0:
            right = 0

        if top < 0:
            top = 0

        if bottom < 0:
            bottom = 0

        if left > self.size_in_tiles.x:
            left = self.size_in_tiles.x

        if right > self.size_in_tiles.x:
            right = self.size_in_tiles.x

        if top > self.size_in_tiles.y:
            top = self.size_in_tiles.y

        if bottom > self.size_in_tiles.y:
            bottom = self.size_in_tiles.y

        for y in range(top, bottom):
            for x in range(left, right):
                tile = self.tiles[self.matrix[y][x]]
                surface.blit(self.image, (x * self.tile_size.x + scroll.x,
                                          y * self.tile_size.y + scroll.y),
                             list(tile.get_tuple()) + list(self.tile_size.get_tuple()))
