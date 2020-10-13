import numpy as np

import time

from my_libs import Rect, Vector2D


class SpawnExample:
    def __init__(self, object_, min_, max_, duration, area, shift):
        self.object_ = object_
        self.min_ = min_
        self.max_ = max_
        self.area = area  # spawn-area
        self.shift = shift
        self.spawning = True
        self.start = time.monotonic()
        self.duration = duration
        self.count = 0


class Spawn:  # spawns only copy of object
    def __init__(self, containers):
        self.containers = containers
        self.examples = dict()

    def spawn(self, obj, return_obj=False):
        new_obj = obj.copy()
        self.containers[obj.container].append(new_obj)

        if return_obj:
            return new_obj

    def spawn_random(self, count, area, obj, shift=Vector2D(0, 0), return_obj=False):
        objects = list()
        collision_rect = obj.get_collision_rect()
        for i in range(count):
            new_obj = obj.copy()
            new_obj.position = self.define_new_position(collision_rect, area, shift)
            objects.append(new_obj)
            self.containers[obj.container].append(new_obj)

        if return_obj:
            return objects

    def spawn_rect(self, rect, obj, shift=Vector2D(0, 0), edges=True, return_obj=False):
        collision_rect = obj.get_collision_rect()

        size = Vector2D(rect.width // (collision_rect.width + 2 * shift.x),
                        rect.height // (collision_rect.height + 2 * shift.y))

        objects = list()
        for j in range(int(size.y)):
            for i in range(int(size.x)):
                if edges:
                    if (j != 0) and (j != int(size.y) - 1) and (i != 0) and (i != int(size.x) - 1):
                        continue

                new_obj = obj.copy()
                new_obj.position = Vector2D(rect.left + (i + 0.5) * (collision_rect.width + 2 * shift.x),
                                            rect.top + (j + 0.5) * (collision_rect.height + 2 * shift.y))
                objects.append(new_obj)
                self.containers[obj.container].append(new_obj)

        if return_obj:
            return objects

    def define_new_position(self, rect, area, shift):
        new_position = Vector2D(np.random.uniform(area.left, area.right),
                                np.random.uniform(area.top, area.bottom))

        if sum([len(self.containers[container_name]) for container_name in self.containers]) == 0:
            return new_position

        new_rect = Rect(new_position.x, new_position.y,
                        rect.width + 2 * shift.x, rect.height + 2 * shift.y, isCenter=True)

        for container_name in self.containers:
            for obj in self.containers[container_name]:
                if new_rect.intersects(obj.get_collision_rect()):
                    return self.define_new_position(rect, area, shift)
        return new_position

    # removes 1 object and check if it is involved in periodic spawn
    def safe_remove(self, obj):
        if obj.family in self.examples.keys():
            self.examples[obj.family].count -= 1
        self.remove(obj)

    def remove(self, obj):
        self.containers[obj.container].remove(obj)

    def remove_family(self, container_name, family):
        for obj in self.containers[container_name]:
            if obj.family == family:
                self.remove(obj)

    def add_example(self, example):
        self.examples[example.object_.family] = example

    def update(self):
        for name, example in self.examples.items():
            if time.monotonic() - example.start > example.duration or example.count < example.min_:
                self.remove_family(example.object_.container, example.object_.family)
                self.spawn_random(example.max_, example.area, example.object_, example.shift, return_obj=True)
                example.count = example.max_
                example.start = time.monotonic()
