from animationManager import AnimationManager

class Entity:

    def __init__(self, animanager, x, y, speed, health, strength):
        self.animanager = animanager
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.strength = strength

    def move_x(self, time):
        self.x += self.speed * time

    def move_y(self, time):
        self.y += self.speed * time

    def control(self):
        pass

    def update(self, time):
        self.animanager.tick(time)

    def draw(self, surface):
        self.animanager.draw(surface, self.x, self.y)