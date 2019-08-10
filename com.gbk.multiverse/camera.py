from my_libs import Rect, Vector2D

class Camera:
    def __init__(self, screen_size, coefficient):
        self.center = Vector2D(screen_size.x / 2, screen_size.y / 2)
        self.coefficient = coefficient
        self.frame = Rect(self.center.x, self.center.y,
                          screen_size.x / self.coefficient, screen_size.y / self.coefficient, isCenter=True)
        self.bias = 16 * 2

    def update(self, position):
        self.frame.move_to(self.center.x - position.x, self.center.y - position.y)
