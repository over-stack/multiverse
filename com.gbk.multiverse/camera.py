
class Camera:

    def __init__(self, screen_size):
        self.center = [screen_size[0] // 2, screen_size[1] // 2]
        self.frame = [self.center[0], self.center[1]]

    def update(self, position):
        self.frame = [self.center[0] - position[0], self.center[1] - position[1]]