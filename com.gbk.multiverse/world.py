from pygame import image, Rect
import pygame

class World:

    def __init__(self, filename, size, tile_size):
        self.image = image.load(filename)
        self.size = size
        self.size_in_tiles = [size[0] // tile_size[0], size[1] // tile_size[1]]
        self.tile_size = tile_size
        self.matrix = self.generate_matrix()
        self.tiles = dict()

        self.game_time = 0
        self.sun_brightness = 100
        self.sun = (0, 0, 0, 255)

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
        return [[0 for _ in range(self.size_in_tiles[0])] for _ in range(self.size_in_tiles[1])]

    def draw(self, surface, scroll, position, width, height):

        left = int((position[0] - width) // self.tile_size[0])
        right = int((position[0] + width) // self.tile_size[0])
        top = int((position[1] - height) // self.tile_size[1])
        bottom = int((position[1] + height) // self.tile_size[1])

        if left < 0:
            left = 0

        if right < 0:
            right = 0

        if top < 0:
            top = 0

        if bottom < 0:
            bottom = 0

        if left > self.size_in_tiles[0]:
            left = self.size_in_tiles[0]

        if right > self.size_in_tiles[0]:
            right = self.size_in_tiles[0]

        if top > self.size_in_tiles[1]:
            top = self.size_in_tiles[1]

        if bottom > self.size_in_tiles[1]:
            bottom = self.size_in_tiles[1]

        for y in range(top, bottom):
            for x in range(left, right):
                tile = self.tiles[self.matrix[y][x]]
                surface.blit(self.image, (x * self.tile_size[0] + scroll[0],
                                          y * self.tile_size[1] + scroll[1]), tile + self.tile_size)