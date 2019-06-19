import pygame
from animationManager import AnimationManager

class Object:

    def __init__(self, animanager, position, id, max_health = 100):
        self.animanager = animanager
        self.position = position
        self.collision = True

        first_animation = list(self.animanager.animations.values())[0]
        self.width = first_animation.width
        self.height = first_animation.height
        self.depth = first_animation.depth

        self.max_health = max_health
        self.health = max_health

        self.id = id

    def update(self, time):
        self.animanager.tick(time)

    def draw(self, surface, cam_frame):
        position = [self.position[0] + cam_frame[0], self.position[1] + cam_frame[1]]
        self.animanager.draw(surface, position)

        health_line_width = 40
        scaled_health = self.health / (self.max_health / health_line_width)
        health_color = (0, 255, 0) # GREEN
        if 25.0 * (health_line_width / 100) <= scaled_health <= 75.0 * (health_line_width / 100): # %
            health_color = (255, 255, 0) # YELLOW
        elif scaled_health < 25:
            health_color= (255, 0, 0) # BLUE

        pygame.draw.rect(surface, health_color,
                         (position[0] - scaled_health / 2, position[1] - self.height / 2, scaled_health, 2))

    def in_area(self, area):

        intersects = True

        left = self.position[0] - self.width / 2
        right = left + self.width
        top = self.position[1] - self.height / 2
        bottom = top + self.height / 2

        if top > area[1] + area[3] or bottom < area[1]:
            intersects = False

        if right < area[0] or left > area[0] + area[2]:
            intersects = False

        return intersects