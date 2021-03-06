import string
import random

import my_libs
from my_libs import Rect, Vector2D

from world import World
from object import Object
from entity import Entity
from decoration import Decoration


# map code

class Encoder:
    def __init__(self, tile_size, camera_size, examples, map_codes):
        self.tile_size = tile_size
        self.camera_size = camera_size
        self.codes = dict()
        self.codes['self'] = 'i'  # self-code
        self.codes['right'] = '>'
        self.codes['left'] = '<'
        for example in examples:
            if example.family not in self.codes:
                free_symbols = list(filter(lambda x: x not in self.codes.values(), my_libs.OBJECT_SYMBOLS))
                code = random.choice(free_symbols)
                self.codes[example.family] = code

        values = list(self.codes.values())
        VALUES = [i.upper() for i in values]
        one_hot_codes = values + VALUES + map_codes
        self.one_hot_encoder = dict()
        for i in range(len(one_hot_codes)):
            self.one_hot_encoder[one_hot_codes[i]] = i / len(one_hot_codes)

    def encode(self, map_, self_id, objects, position, print_=False):
        map_ = map_
        rect = Rect(position.x, position.y, self.camera_size.x, self.camera_size.y, isCenter=True)
        for object_ in objects:
            code = self.codes[object_.family]
            if object_.id_ == self_id:
                code = self.codes['self']
            if object_.health < 30:
                code = code.upper()

            if object_.type_ == 'entity':
                direction = object_.get_direction()

            obj_rect = object_.get_rect()
            obj_rect.move(-rect.left, -rect.top)
            tile_rect = Rect(int(obj_rect.left // self.tile_size.x), int(obj_rect.top // self.tile_size.y),
                             int(obj_rect.width // self.tile_size.x), int(obj_rect.height // self.tile_size.y))
            for i in range(tile_rect.top, tile_rect.top + tile_rect.height):
                for j in range(tile_rect.left, tile_rect.left + tile_rect.width):
                    i = max([i, 0])
                    i = min([i, len(map_) - 1])
                    j = max([j, 0])
                    j = min([j, len(map_[0]) - 1])

                    map_[i][j] = code

                    if object_.type_ == 'entity':
                        if (j == tile_rect.left or j == 0) and direction == 'left':
                            map_[i][j] = self.codes['left']
                        elif (j == tile_rect.left + tile_rect.width - 1 or j == len(
                                map_[0]) - 1) and direction == 'right':
                            map_[i][j] = self.codes['right']

        if print_:
            print_map_ = [''.join(i) + '\n' for i in map_]
            with open('map3.txt', 'w') as f:
                f.writelines(print_map_)

        return self.one_hot_encoding(map_)

    def one_hot_encoding(self, features):
        features = [[self.one_hot_encoder[j] for j in features[i]] for i in range(len(features))]
        return features
