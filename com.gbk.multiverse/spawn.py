import random
import numpy as np

from object import Object
from decoration import Decoration
from entity import Entity

from my_libs import Rect, Vector2D


class Spawn:  # spawns only copy of object
    def __init__(self, containers):
        self.containers = containers

    def spawn(self, container_name, obj, return_obj=False):
        new_obj = obj.copy()
        self.containers[container_name].append(new_obj)

        if return_obj:
            return new_obj

    def spawn_rect(self, container_name, rect, obj, shift=None, edges=True, return_id=False):
        if shift is None:
            col_rect = obj.get_collision_rect()
            shift = Vector2D(col_rect.width / 2, col_rect.height / 2)

        obj_rect = obj.get_collision_rect()
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
        self.containers[container_name].extend(objects)

        if return_id:
            return self.get_id(objects)

    def spawn_random(self, container_name, count, area, obj, shift=None, return_id=False):
        if shift is None:
            col_rect = obj.get_collision_rect()
            shift = Vector2D(col_rect.width / 2, col_rect.height / 2)

        objects = list()
        rects = list()

        for i in range(count):
            objects.append(obj.copy())
            objects[-1].position = self.spawn_new_position(area, rects, shift)
            rects.append(objects[-1].get_collision_rect())
        self.containers[container_name].extend(objects)

        if return_id:
            return self.get_id(objects)

    def spawn_new_position(self, area, rects, shift):
        new_position = Vector2D(np.random.uniform(area.left, area.right),
                                np.random.uniform(area.top, area.bottom))
        if len(rects) == 0:
            return new_position

        new_rect = Rect(new_position.x, new_position.y,
                        rects[0].width + 2 * shift.x, rects[0].height + 2 * shift.y, isCenter=True)
        for rect in rects:
            if new_rect.intersects(rect):
                return self.spawn_new_position(area, rects, shift)
        return new_position

    def get_id(self, objects):
        ids = list()
        for object in objects:
            ids.append(object.id_)
        return ids
