import random
from pygame import image, Rect

import my_libs
from my_libs import Rect, Vector2D


class World:
    def __init__(self, filename, size, tile_size):
        self.image = image.load(filename)
        self.size = size
        self.size_in_tiles = Vector2D(size.x // tile_size.x, size.y // tile_size.y)
        self.tile_size = tile_size

        self.matrix = list()
        self.tiles = dict()
        self.decoder = dict()
        self.encoder = dict()

        self.decoder['0'] = 'None'
        self.encoder['None'] = '0'

        # self.heat_map = list()
        # self.water_map = list()

        self.add_tile(name='dirt', position=Vector2D(208, 288))
        self.add_tile(name='red', position=Vector2D(368, 400))
        self.add_tile(name='dirt1', position=Vector2D(272, 384))
        self.add_tile(name='dirt2', position=Vector2D(286, 384))
        self.add_tile(name='dirt_to_red', position=Vector2D(302, 384))
        self.add_tile(name='dirt_to_red2', position=Vector2D(302, 400))
        self.add_tile(name='red1', position=Vector2D(302, 416))
        self.add_tile(name='dirt3', position=Vector2D(302, 432))
        self.add_tile(name='dirt4', position=Vector2D(208, 368))
        self.add_tile(name='dirt5', position=Vector2D(240, 368))
        self.add_tile(name='dirt6', position=Vector2D(208, 400))
        self.add_tile(name='dirt7', position=Vector2D(240, 400))
        self.add_tile(name='dirt8', position=Vector2D(208, 432))
        self.add_tile(name='dirt9', position=Vector2D(240, 432))
        self.add_tile(name='fence', position=Vector2D(0, 0))

    def generate_world(self):
        map_ = [[self.encoder['dirt'] for _ in range(self.size_in_tiles.x)] for _ in range(self.size_in_tiles.y)]
        map_ = [''.join(i) + '\n' for i in map_]
        with open('map0.txt', 'w') as f:
            f.writelines(map_)
        return 'map0.txt'

    def load_map(self, path):
        with open(path, 'r') as f:
            self.matrix = f.readlines()

    def add_tile(self, name, position):
        self.tiles[name] = position
        free_symbols = list(filter(lambda x: x not in self.decoder, my_libs.MAP_SYMBOLS))
        code = random.choice(free_symbols)
        self.decoder[code] = name
        self.encoder[name] = code

    def get_world_around(self, position, camera):
        rect = Rect(position.x // self.tile_size.x, position.y // self.tile_size.y,
                    (camera.frame.width // self.tile_size.x), (camera.frame.height // self.tile_size.y),
                    isCenter=True)

        map_ = [['0' for _ in range(int(rect.width))] for _ in range(int(rect.height))]

        self.fix_edges(rect)

        for y in range(int(rect.top), int(rect.bottom)):
            for x in range(int(rect.left), int(rect.right)):
                map_[y - int(rect.top)][x - int(rect.left)] = self.matrix[y][x]

        return map_

    def draw(self, surface, position, camera):
        rect = Rect(position.x // self.tile_size.x, position.y // self.tile_size.y,
                    (camera.frame.width // self.tile_size.x) + 2, (camera.frame.height // self.tile_size.y) + 4,
                    isCenter=True)  # magic numbers

        self.fix_edges(rect)

        for y in range(int(rect.top), int(rect.bottom)):
            for x in range(int(rect.left), int(rect.right)):
                tile = self.tiles[self.decoder[self.matrix[y][x]]]
                surface.blit(self.image, (x * self.tile_size.x + camera.get_scroll().x,
                                          y * self.tile_size.y + camera.get_scroll().y),
                             list(tile.get_tuple()) + list(self.tile_size.get_tuple()))

    def fix_edges(self, rect):
        rect.left = max([rect.left, 0])
        rect.right = max([rect.right, 0])
        rect.top = max([rect.top, 0])
        rect.bottom = max([rect.bottom, 0])

        rect.left = min([rect.left, self.size_in_tiles.x])
        rect.right = min([rect.right, self.size_in_tiles.x])
        rect.top = min([rect.top, self.size_in_tiles.y])
        rect.bottom = min([rect.bottom, self.size_in_tiles.y])

    def get_area(self, shift=0):
        return Rect(shift, shift, self.size.x - 2 * shift, self.size.y - 2 * shift)

    def get_codes(self):
        return list(self.decoder.keys())