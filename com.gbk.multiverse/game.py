import sys
import itertools
import pygame
from animationManager import AnimationManager
from entity import Entity
from world import World
from camera import Camera
from decoration import Decoration

import numpy as np

class Game:

    def __init__(self, screen_size, title):
        self.screen_size = screen_size
        self.title = title

        pygame.init()
        self.window = pygame.display.set_mode(screen_size, pygame.HWSURFACE|pygame.DOUBLEBUF)
        self.canvas = self.window.copy()

        pygame.display.set_caption(title)

        self.fps = 60
        self.vision_radius = self.screen_size[0] // 3

        self.decorations = list()
        self.entities = list()
        self.free_id = 0

        self.resources_dir = 'resources/gothicvania patreon collection/'
        self.resources_dir1 = 'resources/tiny-RPG-forest-files/PNG/environment/'

    def new(self):

        self.animation_managers()

        self.cam = Camera(screen_size=self.screen_size)

        self.game_world = World(filename=self.resources_dir1 + 'tileset.png', size=(20000, 20000), tile_size=(16, 16))
        self.game_world.add_tile(position=(208, 288), code=0)

        random_positions = np.random.rand(10, 2) * 1000

        for i in range(10):
            self.decorations.append(Decoration(animanager=self.anim_dec,
                                                       position=list(random_positions[i, :]),
                                                       max_health=1000, id=self.free_id))
            self.decorations[i].have_not_death_anim = True
            self.free_id += 1

        self.hero = Entity(animanager=self.anim_hero, position=[800, 400], speed=10, max_health=100, strength=7, id=self.free_id)
        self.hero.have_not_death_anim = True

        self.entities.append(self.hero)
        self.free_id += 1

        dog = Entity(animanager=self.anim_dog, position=[1100, 450], speed=-12, max_health=80, strength=14, id=self.free_id)
        dog.have_not_death_anim = True
        dog.acceleration[0] = dog.speed / 2

        self.entities.append(dog)
        self.free_id += 1

        ghost = Entity(animanager=self.anim_ghost, position=[700, 250], speed=10, max_health=200, strength=20, id=self.free_id)

        self.entities.append(ghost)
        self.free_id += 1

    def run(self):

        Clock = pygame.time.Clock()

        run = True
        while run:
            Clock.tick(self.fps)

            time = Clock.get_time()
            time = time / 80  # game speed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()

            for ent in self.entities:
                ent.vision(self.entities + self.decorations)

            self.hero.control(keys)

            for ent in self.entities:
                ent.check_collision(self.entities + self.decorations)

            self.update(time)

            self.window.fill((0, 0, 0))  # Makes black window

            self.draw()

        pygame.quit()

    def update(self, time):

        for dec in self.decorations:
            dec.update(time)

        for ent in self.entities:
            if ent.health <= 0:
                ent.die()
            if not ent.alive:
                self.entities.remove(ent)

            ent.update(time)

        self.cam.update(self.hero.position)
        pygame.display.update()

    def draw(self):

        self.window.fill((0, 0, 0))  # Makes black window
        self.canvas.fill((0, 0, 0))

        objects = self.decorations + self.entities

        objects.sort(key=lambda obj: obj.position[1])  # sorting objects by y axis

        self.game_world.draw(self.canvas, self.cam.frame, self.hero.position, radius=self.vision_radius)  # draw map

        for obj in objects:  # draw objects # the nearest
            if self.hero.position[0] - self.vision_radius <= obj.position[0] <= self.hero.position[0] + self.vision_radius:
                if self.hero.position[1] - self.vision_radius <= obj.position[1] <= self.hero.position[1] + self.vision_radius:
                    obj.draw(self.canvas, self.cam.frame)

        k = 2
        self.window.blit(pygame.transform.scale(self.canvas, [self.screen_size[0] * k,
                                                              self.screen_size[1] * k]),
                         (-self.screen_size[0] // k, -self.screen_size[1] // k))

    def animation_managers(self):

        self.anim_dec = AnimationManager()
        self.anim_hero = AnimationManager()
        self.anim_dog = AnimationManager()
        self.anim_ghost = AnimationManager()

        self.anim_dec.create(name='stay', filename=self.resources_dir1 + '/sliced-objects/tree-pink.png',
                        cols=1, rows=1, count=1, speed=0)

        self.anim_hero.create(name='stay', filename=self.resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-idle.png',
                         cols=4, rows=1, count=4, speed=0.5, looped=True)
        self.anim_hero.create(name='attack', filename=self.resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-attack.png',
                         cols=6, rows=1, count=6, speed=0.5)
        self.anim_hero.create(name='walk', filename=self.resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-run.png',
                         cols=12, rows=1, count=12, speed=0.5, looped=True)

        self.anim_ghost.create(name='stay', filename=self.resources_dir + 'Ghost-Files/PNG/ghost-idle.png',
                          cols=7, rows=1, count=7, speed=0.5, looped=True)
        self.anim_ghost.create(name='walk', filename=self.resources_dir + 'Ghost-Files/PNG/ghost-shriek.png',
                          cols=4, rows=1, count=4, speed=0.5, looped=True)
        self.anim_ghost.create(name='death', filename=self.resources_dir + 'Ghost-Files/PNG/ghost-vanish.png',
                          cols=7, rows=1, count=7, speed=0.5, looped=False)

        self.anim_dog.create(name='stay', filename=self.resources_dir + 'Hell-Hound-Files/PNG/hell-hound-idle.png',
                        cols=6, rows=1, count=6, speed=0.5, looped=True)
        self.anim_dog.create(name='walk', filename=self.resources_dir + 'Hell-Hound-Files/PNG/hell-hound-walk.png',
                        cols=12, rows=1, count=12, speed=0.5, looped=True)

if __name__ == '__main__':
    game = Game([1280, 720], 'Multiverse')

    game.new()
    game.run()