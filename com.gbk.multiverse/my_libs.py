import string
import numpy as np

from copy import deepcopy

MAP_SYMBOLS = list(filter(lambda x: x not in string.ascii_letters, string.printable))
OBJECT_SYMBOLS = list(string.ascii_lowercase)


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def __repr__(self):
        return f'X: {self.x}, Y: {self.y}'

    def length(self):
        return (self.x * self.x + self.y * self.y) ** 0.5

    def get_tuple(self):
        return self.x, self.y

    def is_null(self):
        if self.x == 0 and self.y == 0:
            return True

    def copy(self):
        return deepcopy(self)


class Rect:
    def __init__(self, x, y, width, height, isCenter=False):
        self.width = width
        self.height = height
        self.center = Vector2D(0, 0)
        self.topleft = Vector2D(0, 0)
        self.move_to(x, y, isCenter)
        #self.last_intersection = Vector2D(0, 0)

    def __repr__(self):
        return f'Left: {self.left}, Top: {self.top}, Width: {self.width}, Height: {self.height}, Center: {self.center}'

    def intersects(self, rect):
        intersects = True
        if self.top >= rect.bottom or self.bottom <= rect.top:
            intersects = False
        elif self.right <= rect.left or self.left >= rect.right:
            intersects = False

        return intersects

    def move(self, x, y):
        self.left += x
        self.right += x
        self.center.x += x
        self.topleft.x += x

        self.top += y
        self.bottom += y
        self.center.y += y
        self.topleft.y += y

    def move_to(self, x, y, isCenter=False):
        if isCenter:
            self.center.x = x
            self.center.y = y
            self.left = self.center.x - self.width / 2
            self.top = self.center.y - self.height / 2
        else:
            self.center = Vector2D(x + self.width / 2, y + self.height / 2)
            self.left = x
            self.top = y

        self.right = self.left + self.width
        self.bottom = self.top + self.height
        self.topleft.x = self.left
        self.topleft.y = self.top

    def get_tuple(self):
        return self.left, self.top, self.width, self.height

    def distance2d(self, rect):
        return rect.center.x - self.center.x, rect.center.y - self.center.y

    def v2_distance2d(self, rect):
        return (rect.center.x - self.center.x) ** 2 + (rect.center.y - self.center.y) ** 2

    def distance_polar(self, rect):
        a, b = self.distance2d(rect)
        if a == 0:
            if b == 0:
                return 0, 0
            else:
                return np.sign(b) * np.pi / 2, np.sqrt(b*b)
        return np.arctan(b/a), np.sqrt(a*a + b*b)

    def copy(self):
        return deepcopy(self)


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def intersects(self, x, y):
        if (x - self.x)**2 + (y - self.y) ** 2 <= self.radius ** 2:
            return True


class Node:
    def __init__(self, decoration=None, value=None):
        self.decoration = decoration
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def addSorted(self, decoration, value):
        new_node = Node(decoration, value)
        if self.head is None:
            self.head = new_node
            return

        if value < self.head.value:
            new_node.next = self.head
            self.head = new_node
            return

        current = self.head
        while (current):
            if current.next:
                if value < current.next.value:
                    new_node.next = current.next
                    current.next = new_node
                    return
                else:
                    current = current.next
            else:
                current.next = new_node
                return

    def delFirst(self):
        self.head = self.head.next


class InterManager:
    def __init__(self):
        self.ent_table = dict()
        self.dec_table = dict()
        self.circle = Circle(0, 0, 360)
        self.time_ = 0
        self.update_container = dict()
        self.k = 2

    def make_decorations_table(self, entities, decorations):
        for ent in entities:
            self.dec_table[ent] = LinkedList()

        for entity in entities:
            collision_rect = entity.get_collision_rect()
            for decoration in decorations:
                decoration_collision_rect = decoration.get_collision_rect()
                distance = collision_rect.v2_distance2d(decoration_collision_rect)
                speed = entity.speed * self.k
                value = (distance/100) / speed
                self.dec_table[entity].addSorted(decoration, value)

    def make_entities_table(self, entities):
        for ent in entities:
            self.ent_table[ent] = list()

        for i in range(len(entities)):
            position = entities[i].position
            self.circle.x = position.x
            self.circle.y = position.y
            for j in range(i+1, len(entities)):
                ent_position = entities[j].position
                if self.circle.intersects(ent_position.x, ent_position.y):
                    self.ent_table[entities[i]].append(entities[j])
                    self.ent_table[entities[j]].append(entities[i])

    def tick(self, time_):
        self.time_ += time_

    def get_decorations_around(self, entity):
        decorations_around = list()
        node = self.dec_table[entity].head
        while node:
            if node.value <= self.time_:
                print('ooo eh')
                decorations_around.append(node.decoration)
                self.dec_table[entity].delFirst()
                node = node.next
            else:
                break
        self.update_container[entity] = list(decorations_around)
        return decorations_around

    def update(self):
        print([i.head.value for i in self.dec_table.values()])
        for entity in self.update_container.keys():
            collision_rect = entity.get_collision_rect()
            for decoration in self.update_container[entity]:
                decoration_collision_rect = decoration.get_collision_rect()
                distance = collision_rect.v2_distance2d(decoration_collision_rect)
                speed = entity.speed * self.k
                value = self.time_ + (distance / 100) / speed
                self.dec_table[entity].addSorted(decoration, value)
            del self.update_container[entity]
