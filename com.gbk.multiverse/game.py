import numpy as np
import pygame

from camera import Camera
from animationManager import AnimationManager
from world import World
from entity import Entity
from decoration import Decoration
from environment import Environment
from sun import Sun
from spawn import Spawn
from encoder import Encoder
from evolution import Evolution, EvolutionExample

from my_libs import Rect, Vector2D

# fix damage area
# fix animationManager
# do multithreading

class Game:
    def __init__(self, screen_size, title):
        self.screen_size = screen_size
        self.title = title
        self.fps = 60

        pygame.init()
        self.window = pygame.display.set_mode(screen_size.get_tuple(),
                                              pygame.HWSURFACE | pygame.DOUBLEBUF)  # only for draw the canvas
        self.canvas = self.window.copy()  # used to draw

        pygame.display.set_caption(title)

        self.resources = dict()
        self.sheets = dict()
        self.animanagers = dict()
        self.examples = dict()
        self.decorations = dict()
        self.entities = dict()

        self.include_resources()
        self.animation_managers()

        self.cam = Camera(screen_size=self.screen_size, coefficient=2)
        self.spawn = Spawn({'decorations': self.decorations, 'entities': self.entities})
        self.evolution = Evolution(self.spawn)
        self.game_env = Environment()
        self.game_world = World(filename=f'{self.resources["tiny-rpg"]}tileset.png', size=Vector2D(1000, 1000),
                                tile_size=Vector2D(16, 16))
        self.game_world.load_map(self.game_world.generate_world())
        self.sun = Sun(self.cam.frame.width, self.cam.frame.height)

        self.add_examples()
        self.encoder = Encoder(self.game_world.tile_size, Vector2D(self.cam.frame.width, self.cam.frame.height),
                               self.examples.values(), self.game_world.get_codes())
        self.add_decorations()
        self.add_entities()

        self.allow_draw = True

    def include_resources(self):
        self.resources['goth'] = 'resources/gothicvania patreon collection/'
        self.resources['tiny-rpg'] = 'resources/tiny-RPG-forest-files/PNG/environment/'

        self.sheets['tree'] = dict()
        self.sheets['tree']['stay'] = pygame.image.load(f'{self.resources["tiny-rpg"]}/sliced-objects/tree-pink.png')

        self.sheets['hero'] = dict()
        self.sheets['hero']['stay'] = pygame.image.load(
            f'{self.resources["goth"]}Gothic-hero-Files/PNG/gothic-hero-idle.png')
        self.sheets['hero']['attack'] = pygame.image.load(
            f'{self.resources["goth"]}Gothic-hero-Files/PNG/gothic-hero-attack.png')
        self.sheets['hero']['run'] = pygame.image.load(
            f'{self.resources["goth"]}Gothic-hero-Files/PNG/gothic-hero-run.png')

        self.sheets['ghost'] = dict()
        self.sheets['ghost']['stay'] = pygame.image.load(f'{self.resources["goth"]}Ghost-Files/PNG/ghost-idle.png')
        self.sheets['ghost']['walk'] = pygame.image.load(f'{self.resources["goth"]}Ghost-Files/PNG/ghost-shriek.png')
        self.sheets['ghost']['death'] = pygame.image.load(f'{self.resources["goth"]}Ghost-Files/PNG/ghost-vanish.png')

        self.sheets['dog'] = dict()
        self.sheets['dog']['stay'] = pygame.image.load(
            f'{self.resources["goth"]}Hell-Hound-Files/PNG/hell-hound-idle.png')
        self.sheets['dog']['walk'] = pygame.image.load(
            f'{self.resources["goth"]}Hell-Hound-Files/PNG/hell-hound-walk.png')

        self.sheets['demon'] = dict()
        self.sheets['demon']['stay'] = pygame.image.load(
            f'{self.resources["goth"]}demon-Files/PNG/demon-idle.png')
        self.sheets['demon']['attack'] = pygame.image.load(
            f'{self.resources["goth"]}demon-Files/PNG/demon-attack.png')

    def animation_managers(self):
        self.animanagers['tree'] = AnimationManager()
        self.animanagers['tree'].create(name='stay', sheet=self.sheets['tree']['stay'],
                              cols=1, rows=1, count=1, speed=0)

        self.animanagers['hero'] = AnimationManager()
        self.animanagers['hero'].create(name='stay', sheet=self.sheets['hero']['stay'],
                              cols=4, rows=1, count=4, speed=0.2, looped=True)
        self.animanagers['hero'].create(name='attack', sheet=self.sheets['hero']['attack'],
                                        cols=6, rows=1, count=6, speed=0.9)
        self.animanagers['hero'].create(name='walk', sheet=self.sheets['hero']['run'],
                                        cols=12, rows=1, count=12, speed=0.9, looped=True)

        self.animanagers['ghost'] = AnimationManager(defaultFlipped=True)
        self.animanagers['ghost'].create(name='stay', sheet=self.sheets['ghost']['stay'],
                               cols=7, rows=1, count=7, speed=0.5, looped=True)
        self.animanagers['ghost'].create(name='attack', sheet=self.sheets['ghost']['walk'],
                                         cols=4, rows=1, count=4, speed=0.5, looped=False)
        self.animanagers['ghost'].create(name='death', sheet=self.sheets['ghost']['death'],
                                         cols=7, rows=1, count=7, speed=0.5, looped=False)

        self.animanagers['dog'] = AnimationManager(defaultFlipped=True)
        self.animanagers['dog'].create(name='stay', sheet=self.sheets['dog']['stay'],
                             cols=6, rows=1, count=6, speed=0.5, looped=True)
        self.animanagers['dog'].create(name='walk', sheet=self.sheets['dog']['walk'],
                                       cols=12, rows=1, count=12, speed=0.5, looped=True)

        self.animanagers['demon'] = AnimationManager()
        self.animanagers['demon'].create(name='stay', sheet=self.sheets['demon']['stay'],
                                         cols=6, rows=1, count=6, speed=0.5, looped=True)
        self.animanagers['demon'].create(name='attack', sheet=self.sheets['demon']['attack'],
                                         cols=11, rows=1, count=11, speed=0.5, looped=False)

    def add_examples(self):
        tree = Decoration(animanager=self.animanagers['tree'], position=Vector2D(0, 0),
                          max_health=1000, family='tree')
        self.examples['tree'] = tree

        immortal_tree = Decoration(animanager=self.animanagers['tree'], position=Vector2D(0, 0),
                                   max_health=1000, family='tree')
        immortal_tree.immortal = True
        self.examples['immortal_tree'] = immortal_tree

        hero = Entity(animanager=self.animanagers['hero'], position=Vector2D(500, 500), speed=10, max_health=200,
                      strength=20, family='hero')  # family=hero -> main character
        hero.ai = False
        hero.immortal = True
        self.examples['hero'] = hero

        dog = Entity(animanager=self.animanagers['dog'], position=Vector2D(1100, 550), speed=-12, max_health=80,
                     strength=14, family='dog')
        self.examples['dog'] = dog

        ghost = Entity(animanager=self.animanagers['ghost'], position=Vector2D(0, 0), speed=10, max_health=100,
                       strength=20, family='ghost')
        self.examples['ghost'] = ghost

        demon = Entity(animanager=self.animanagers['demon'], position=Vector2D(0, 0), speed=12, max_health=200,
                       strength=40, family='demon')
        self.examples['demon'] = demon

        for example in self.examples.values():
            if example.type_ == 'entity':
                example.generate_random_priorities(env_states=self.game_env.get_states())

        self.evolution.add_example('ghost', EvolutionExample(self.examples['ghost'], min_=2, max_=10,
                                                             area=self.game_world.get_area()))
        self.evolution.add_example('demon', EvolutionExample(self.examples['demon'], min_=2, max_=10,
                                                             area=self.game_world.get_area()))
        # self.evolution.add_example('dog', EvolutionExample(self.examples['dog'], min_=2, max_=5,
        # area=self.game_world.get_area()))

    def add_decorations(self):
        self.spawn.spawn_rect(container_name='decorations', rect=self.game_world.get_area(),
                              obj=self.examples['immortal_tree'], shift=None)
        self.spawn.spawn_random(container_name='decorations', count=50, area=self.game_world.get_area(),
                                obj=self.examples['tree'], shift=Vector2D(15, 15))

    def add_entities(self):
        self.hero = self.spawn.spawn('entities', self.examples['hero'], return_obj=True)
        # self.spawn.spawn('entities', self.examples['dog'])

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(self.fps)
            time = clock.get_time()
            time = time / 80  # game speed
            #time = 2

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.vci(time)
            self.update(time)

            if self.allow_draw:
                self.draw()

        pygame.quit()

    # vision controlling and interaction
    def vci(self, time):
        for ent in self.entities.values():
            # Vision
            area = Rect(ent.get_rect().center.x, ent.get_rect().center.y,
                        self.cam.frame.width, self.cam.frame.height, isCenter=True)
            entities_around = [_ for _ in self.entities.values() if _.get_rect().intersects(area)]
            decorations_around = [_ for _ in self.decorations.values() if _.get_rect().intersects(area)]
            objects_around = entities_around + decorations_around
            objects_around.sort(key=lambda obj: obj.get_rect().bottom)  # sorting objects by y axis
            world_around = self.game_world.get_world_around(ent.get_rect().center, self.cam)
            self.game_env.apply(entity=ent, objects_around=objects_around, world_around=None)

            # Controlling
            if not ent.ai:
                # features = self.encoder.encode(world_around, ent.id_, objects_around, ent.get_rect().center,
                #print_=True)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    exit(0)
                if keys[pygame.K_BACKSPACE]:
                    self.allow_draw = not self.allow_draw
                ent.control(keys, time, objects_around)
            else:
                features = self.encoder.encode(world_around, ent.id_, objects_around, ent.get_rect().center)
                ent.ai_control(features, time, objects_around)

    def update(self, time):
        for dec_id in list(self.decorations):
            self.decorations[dec_id].update(time)
            if not self.decorations[dec_id].alive:
                del self.decorations[dec_id]

        for ent_id in list(self.entities):
            self.entities[ent_id].update(time)
            if not self.entities[ent_id].alive:
                if self.entities[ent_id].family == 'hero':
                    print('You are dead')
                    exit(0)

                self.evolution.delete_id(ent_id)
                del self.entities[ent_id]

        self.evolution.update(time)
        self.cam.update(self.hero.get_rect().center)
        self.sun.update(time)
        pygame.display.update()

    def draw(self):
        self.canvas.fill((0, 0, 0))  # Makes black window

        self.game_world.draw(surface=self.canvas, position=self.hero.get_rect().center, camera=self.cam)
        objects = list(self.decorations.values()) + list(self.entities.values())
        objects.sort(key=lambda obj: obj.get_rect().bottom)  # sorting objects by y axis
        for obj in objects:
            if obj.get_rect().intersects(self.cam.frame):
                obj.draw(self.canvas, self.cam.get_scroll())

                # self.canvas.blit(self.sun.img, (self.cam.frame.topleft.x + self.cam.get_scroll().x,
                #self.cam.frame.topleft.y + self.cam.get_scroll().y))

        self.window.blit(pygame.transform.scale(self.canvas, [self.screen_size.x * self.cam.coefficient,
                                                              self.screen_size.y * self.cam.coefficient]),
                         (-self.cam.frame.width, -self.cam.frame.height))

if __name__ == '__main__':
    game = Game(Vector2D(1280, 720), 'Multiverse')
    game.run()