from my_libs import Rect, Vector2D


class Camera:
    def __init__(self, screen_size, coefficient):
        self.coefficient = coefficient
        self.frame = Rect(screen_size.x / 2, screen_size.y / 2,
                          screen_size.x / self.coefficient, screen_size.y / self.coefficient, isCenter=True)
        self.bias = 16 * 2

    def update(self, center):
        self.frame.move_to(center.x, center.y, isCenter=True)

    def get_scroll(self):
        return Vector2D(-self.frame.center.x + self.frame.width,
                        -self.frame.center.y + self.frame.height)
