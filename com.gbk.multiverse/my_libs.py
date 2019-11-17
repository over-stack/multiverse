import string

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


class Rect:
    def __init__(self, x, y, width, height, isCenter=False):
        self.width = width
        self.height = height
        self.move_to(x, y, isCenter)

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
            self.center = Vector2D(x, y)
            self.left = self.center.x - self.width / 2
            self.top = self.center.y - self.height / 2
        else:
            self.center = Vector2D(x + self.width / 2, y + self.height / 2)
            self.left = x
            self.top = y

        self.right = self.left + self.width
        self.bottom = self.top + self.height
        self.topleft = Vector2D(self.left, self.top)

    def get_tuple(self):
        return self.left, self.top, self.width, self.height