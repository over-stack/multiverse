from animationManager import AnimationManager

class Object:

    def __init__(self, animanager, position):
        self.animanager = animanager
        self.position = position
        self.collision = True

        first_animation = list(self.animanager.animations.values())[0]
        self.width = first_animation.width
        self.height = first_animation.height
        self.depth = first_animation.depth

    def update(self, time):
        self.animanager.tick(time)

    def draw(self, surface, cam_frame):
        position = [self.position[0] + cam_frame[0], self.position[1] + cam_frame[1]]
        self.animanager.draw(surface, position)