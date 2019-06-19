import sys
import pygame
from animationManager import AnimationManager
from entity import Entity
from world import World
from camera import Camera
from decoration import Decoration

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

        self.decorations = []
        self.entities = []

    def new(self):
        self.cam = Camera(screen_size=self.screen_size)

        resources_dir = 'resources/gothicvania patreon collection/'
        resources_dir1 = 'resources/tiny-RPG-forest-files/PNG/environment/'

        self.game_world = World(filename=resources_dir1 + 'tileset.png', size=(2000, 2000), tile_size=(16, 16))
        self.game_world.add_tile(position=(208, 288), code=0)

        anim_dec = AnimationManager()

        anim_dec.create(name='stay', filename=resources_dir1 + '/sliced-objects/tree-pink.png',
                        cols=1, rows=1, count=1, speed=0)

        tree = Decoration(animanager=anim_dec, position=[200, 200], health=100)

        self.decorations.append(tree)

        anim_hero = AnimationManager()

        anim_hero.create(name='stay', filename=resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-idle.png',
                         cols=4, rows=1, count=4, speed=0.5, looped=True)
        anim_hero.create(name='attack', filename=resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-attack.png',
                         cols=6, rows=1, count=6, speed=0.5)
        anim_hero.create(name='walk', filename=resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-run.png',
                         cols=12, rows=1, count=12, speed=0.5, looped=True)

        self.hero = Entity(animanager=anim_hero, position=[700, 100], speed=5, health=100, strength=10)

        self.entities.append(self.hero)

        anim_dog = AnimationManager()

        anim_dog.create(name='stay', filename=resources_dir + 'Hell-Hound-Files/PNG/hell-hound-idle.png',
                        cols=6, rows=1, count=6, speed=0.5, looped=True)
        anim_dog.create(name='walk', filename=resources_dir + 'Hell-Hound-Files/PNG/hell-hound-walk.png',
                        cols=12, rows=1, count=12, speed=0.5, looped=True)

        dog = Entity(animanager=anim_dog, position=[800, 250], speed=7, health=80, strength=14)

        dog.acceleration[0] = -5

        self.entities.append(dog)

        anim_ghost = AnimationManager()

        anim_ghost.create(name='stay', filename=resources_dir + 'Ghost-Files/PNG/ghost-idle.png',
                          cols=7, rows=1, count=7, speed=0.5, looped=True)

        anim_ghost.create(name='walk', filename=resources_dir + 'Ghost-Files/PNG/ghost-shriek.png',
                          cols=4, rows=1, count=4, speed=0.5, looped=True)

        anim_ghost.create(name='death', filename=resources_dir + 'Ghost-Files/PNG/ghost-vanish.png',
                          cols=7, rows=1, count=7, speed=0.5, looped=False)

        ghost = Entity(animanager=anim_ghost, position= [700, 250], speed=7, health=200, strength=20)

        self.entities.append(ghost)

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

            if len(self.entities) >= 3:
                self.entities[2].health -= 1

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

        for obj in objects:  # draw objects
            if self.hero.position[0] - self.vision_radius <= obj.position[0] <= self.hero.position[0] + self.vision_radius:
                if self.hero.position[1] - self.vision_radius <= obj.position[1] <= self.hero.position[1] + self.vision_radius:
                    obj.draw(self.canvas, self.cam.frame)

        k = 2
        self.window.blit(pygame.transform.scale(self.canvas, [self.screen_size[0] * k,
                                                              self.screen_size[1] * k]),
                         (-self.screen_size[0] // k, -self.screen_size[1] // k))

if __name__ == '__main__':
    game = Game([1280, 720], 'Multiverse')

    game.new()
    game.run()