import string
import numpy as np

MAP_SYMBOLS = list(filter(lambda x: x not in string.ascii_letters, string.printable))
OBJECT_SYMBOLS = list(string.ascii_lowercase)


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f'X: {self.x}, Y: {self.y}'

    def get_tuple(self):
        return self.x, self.y

    def is_null(self):
        if self.x == 0 and self.y == 0:
            return True


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

    def distance_polar(self, rect):
        a, b = self.distance2d(rect)
        if a == 0:
            if b == 0:
                return 0, 0
            else:
                return np.sign(b) * np.pi / 2, np.sqrt(b*b)
        return np.arctan(b/a), np.sqrt(a*a + b*b)


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def intersects(self, x, y):
        if (x - self.x)**2 + (y - self.y) ** 2 <= self.radius ** 2:
            return True


class InterManager:
    def __init__(self):
        self.table = dict()
        self.circle = Circle(0, 0, 360)

    def make_table(self, objects):
        for obj in objects:
            self.table[obj] = list()

        for i in range(len(objects)):
            position = objects[i].position
            self.circle.x = position.x
            self.circle.y = position.y
            for j in range(i+1, len(objects)):
                obj_position = objects[j].position
                if self.circle.intersects(obj_position.x, obj_position.y):
                    self.table[objects[i]].append(objects[j])
                    self.table[objects[j]].append(objects[i])

