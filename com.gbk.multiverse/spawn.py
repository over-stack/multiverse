import random
import numpy as np

from object import Object
from decoration import Decoration
from entity import Entity

from my_libs import Rect, Vector2D

class Spawn:
    def __init__(self):
        pass

    def spawn_rect(self, rect, obj, shift, edges=True):
        obj_rect = obj.get_collision_rect()
        free_id = obj.id_

        objects = list()
        size = Vector2D(rect.width // (obj_rect.width + shift.x),
                        rect.height // (obj_rect.height + shift.y))
        for j in range(int(size.y)):
            for i in range(int(size.x)):
                if edges:
                    if (j != 0) and (j != int(size.y) - 1) and (i != 0) and (i != int(size.x) - 1):
                        continue
                objects.append(obj.copy())
                objects[-1].position = Vector2D(rect.left + i * (obj_rect.width + shift.x),
                                                rect.top + j * (obj_rect.height + shift.y))
                objects[-1].id_ = free_id
                free_id += 1

        return objects

    def spawn_random(self, rect, obj, shift, count):
        pass
        # random_positions = np.random.rand(20, 2) * 1000
