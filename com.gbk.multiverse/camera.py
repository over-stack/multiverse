
class Camera:
    def __init__(self, screen_size, coef):
        self.center = [screen_size[0] / 2, screen_size[1] / 2]
        self.frame = [self.center[0], self.center[1]]
        self.screen_size = screen_size
        self.coef = coef
        self.width = self.screen_size[0] / self.coef
        self.height = self.screen_size[1] / self.coef
        self.bias = 16 * 2  # only for drawing # make to object self draw rect

    def update(self, position):
        self.frame = [self.center[0] - position[0], self.center[1] - position[1]]