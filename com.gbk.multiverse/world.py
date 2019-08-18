import random
import numpy as np
from pygame import image, Rect
import pygame

from my_libs import Rect, Vector2D

class World:
    def __init__(self, filename, size, tile_size, filepath=''):
        self.image = image.load(filename)
        self.size = size
        self.size_in_tiles = Vector2D(size.x // tile_size.x, size.y // tile_size.y)
        self.tile_size = tile_size
        filepath = ''
        if len(filepath) == 0:
            filepath = self.generate_world()
        with open(filepath, 'r') as f:
            self.matrix = f.readlines()

        self.tiles = dict()

        self.heat_map = list()
        self.water_map = list()

        self.add_tile(position=Vector2D(208, 288), code='a')  # dirt
        self.add_tile(position=Vector2D(368, 400), code='b')  # red
        self.add_tile(position=Vector2D(272, 384), code='c')
        self.add_tile(position=Vector2D(286, 384), code='d')
        self.add_tile(position=Vector2D(302, 384), code='e')  # dirt to red
        self.add_tile(position=Vector2D(302, 400), code='f')  # dirt to red
        self.add_tile(position=Vector2D(302, 416), code='g')  # red
        self.add_tile(position=Vector2D(302, 432), code='h')  # dirt
        self.add_tile(position=Vector2D(208, 368), code='1')
        self.add_tile(position=Vector2D(240, 368), code='2')
        self.add_tile(position=Vector2D(208, 400), code='3')
        self.add_tile(position=Vector2D(240, 400), code='4')
        self.add_tile(position=Vector2D(208, 432), code='5')
        self.add_tile(position=Vector2D(240, 432), code='6')

    def generate_world(self):
        map_ = [['a' for _ in range(self.size_in_tiles.x)] for _ in range(self.size_in_tiles.y)]
        for i in range(500):
            choice = Vector2D(random.randint(2, self.size_in_tiles.x - 1), random.randint(2, self.size_in_tiles.y - 1))
            map_[choice.y][choice.x] = 'b'
            map_[choice.y - 2][choice.x - 2] = 'c'
            map_[choice.y - 2][choice.x - 1] = 'd'
        map_ = [''.join(i) + '\n' for i in map_]
        with open('map0.txt', 'w') as f:
            f.writelines(map_)

        return 'map0.txt'

    def get_world_around(self, position):
        pass

    def add_tile(self, position, code):
        self.tiles[code] = position

    def draw(self, surface, position, camera):
        rect = Rect(position.x // self.tile_size.x, position.y // self.tile_size.y,
                    (camera.frame.width // self.tile_size.x) + 2, (camera.frame.height // self.tile_size.y) + 2,
                    isCenter=True)

        if rect.left < 0:
            rect.left = 0
        if rect.right < 0:
            rect.right = 0
        if rect.top < 0:
            rect.top = 0
        if rect.bottom < 0:
            rect.bottom = 0

        if rect.left > self.size_in_tiles.x:
            rect.left = self.size_in_tiles.x
        if rect.right > self.size_in_tiles.x:
            rect.right = self.size_in_tiles.x
        if rect.top > self.size_in_tiles.y:
            rect.top = self.size_in_tiles.y
        if rect.bottom > self.size_in_tiles.y:
            rect.bottom = self.size_in_tiles.y

        for y in range(int(rect.top), int(rect.bottom)):
            for x in range(int(rect.left), int(rect.right)):
                tile = self.tiles[self.matrix[y][x]]
                surface.blit(self.image, (x * self.tile_size.x + camera.get_scroll().x,
                                          y * self.tile_size.y + camera.get_scroll().y),
                             list(tile.get_tuple()) + list(self.tile_size.get_tuple()))
