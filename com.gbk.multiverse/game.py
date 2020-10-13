import numpy as np
import pygame

from camera import Camera
from animationManager import AnimationManager
from world import World
from entity import Entity
from decoration import Decoration
from environment import Environment
from sun import Sun
from spawn import Spawn, SpawnExample
from evolution import Evolution, EvolutionExample
from genome import Genome

from my_libs import Rect, Vector2D

# add spawn_rect by count
# shift in spawn = border
# make families instead of example_name
# add map limits for moving
# optimize loops
# clear imports
# add multi-threading (evolution, spawn)
# add simple rendering (learn mode)

# fix damage and collision area   (custom collision)
# fix random bag with map
# fix animationManager

# do not spawn on other objects
# animation time
# add camera scaling
# add camera attack effects
# add pause
# add genetic history
# add long range weapons
# procedural generation
# add items and inventory system
# add sounds and music
# add serialization
# add gui


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

        self.hero = None

        self.resources = dict()
        self.sheets = dict()
        self.animanagers = dict()
        self.examples = dict()
        self.decorations = list()
        self.entities = list()
        self.genomes_files = dict()

        self.include_resources()
        self.animation_managers()

        self.cam = Camera(screen_size=self.screen_size, coefficient=2)
        self.spawn = Spawn({'decorations': self.decorations, 'entities': self.entities})
        self.evolution = Evolution(self.spawn)
        #self.game_env = Environment()
        self.game_world = World(filename=f'{self.resources["tiny-rpg"]}tileset.png', size=Vector2D(810, 800),
                                tile_size=Vector2D(16, 16))
        self.game_world.load_map(self.game_world.generate_world())
        self.sun = Sun(self.cam.frame.width, self.cam.frame.height)

        self.add_examples()
        #self.encoder = Encoder(self.game_world.tile_size, Vector2D(self.cam.frame.width, self.cam.frame.height),
                               #self.examples.values(), self.game_world.get_codes())

        self.add_decorations()
        self.add_entities()

        self.allow_draw = True
        self.tree_count = 0 #######################
        self.tree_start = 0

        self.train = list()

    def include_resources(self):
        self.resources['goth'] = 'resources/gothicvania patreon collection/'
        self.resources['tiny-rpg'] = 'resources/tiny-RPG-forest-files/PNG/environment/'

        self.sheets['tree'] = dict()
        self.sheets['tree']['stay'] = pygame.image.load(f'{self.resources["tiny-rpg"]}/sliced-objects/tree-pink.png')

        self.sheets['tree-dried'] = dict()
        self.sheets['tree-dried']['stay'] = pygame.image.load(f'{self.resources["tiny-rpg"]}/sliced-objects/tree-dried.png')

        self.sheets['monument'] = dict()
        self.sheets['monument']['stay'] = pygame.image.load(f'{self.resources["tiny-rpg"]}/sliced-objects/rock-monument.png')

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

        self.sheets['hell-beast'] = dict()
        self.sheets['hell-beast']['stay'] = pygame.image.load(
            f'{self.resources["goth"]}Hell-Beast-Files\PNG\with-stroke\hell-beast-idle.png')
        self.sheets['hell-beast']['attack'] = pygame.image.load(
            f'{self.resources["goth"]}Hell-Beast-Files\PNG\with-stroke\hell-beast-breath.png')

        self.genomes_files['genome1'] = 'neural_network\weights\weights.npy'

    def animation_managers(self):
        self.animanagers['tree'] = AnimationManager()
        self.animanagers['tree'].create(name='stay', sheet=self.sheets['tree']['stay'],
                                        cols=1, rows=1, count=1, speed=0)

        self.animanagers['tree-dried'] = AnimationManager()
        self.animanagers['tree-dried'].create(name='stay', sheet=self.sheets['tree-dried']['stay'],
                                        cols=1, rows=1, count=1, speed=0)

        self.animanagers['monument'] = AnimationManager()
        self.animanagers['monument'].create(name='stay', sheet=self.sheets['monument']['stay'],
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

        self.animanagers['demon'] = AnimationManager(defaultFlipped=True)
        self.animanagers['demon'].create(name='stay', sheet=self.sheets['demon']['stay'],
                                         cols=6, rows=1, count=6, speed=0.5, looped=True)
        self.animanagers['demon'].create(name='attack', sheet=self.sheets['demon']['attack'],
                                         cols=11, rows=1, count=11, speed=0.5, looped=False)

        self.animanagers['hell-beast'] = AnimationManager(defaultFlipped=True)
        self.animanagers['hell-beast'].create(name='stay', sheet=self.sheets['hell-beast']['stay'],
                                         cols=6, rows=1, count=6, speed=0.5, looped=True)
        self.animanagers['hell-beast'].create(name='attack', sheet=self.sheets['hell-beast']['attack'],
                                         cols=4, rows=1, count=4, speed=0.5, looped=False)

    def add_examples(self):
        hero = Entity(animanager=self.animanagers['hero'], speed=10, max_health=1000,
                      strength=100, vision_area=Vector2D(self.cam.frame.width, self.cam.frame.height),
                      family='hero')  # family=hero -> main character
        hero.ai = False
        hero.immortal = True
        hero.strength = 100000
        hero.position = Vector2D(100, 100)
        #hero.alive = True
        #hero.isCollision = True
        #hero.satiety_speed = 0
        #hero.friends.append('hell-beast')
        #hero.make_ghost()
        self.examples['hero'] = hero

        tree = Decoration(animanager=self.animanagers['tree'], max_health=1000, family='tree')
        self.examples['tree'] = tree

        tree_dried = Decoration(animanager=self.animanagers['tree-dried'], max_health=1000, family='tree-dried')
        self.examples['tree-dried'] = tree_dried

        immortal_tree = Decoration(animanager=self.animanagers['tree'], max_health=1000, family='immortal-tree')
        immortal_tree.immortal = True
        self.examples['immortal-tree'] = immortal_tree

        monument = Decoration(animanager=self.animanagers['monument'], max_health=5000, family='monument')
        self.examples['monument'] = monument

        dog = Entity(animanager=self.animanagers['dog'], speed=-12, max_health=80, strength=14,
                     vision_area=Vector2D(self.cam.frame.width, self.cam.frame.height), family='dog')
        self.examples['dog'] = dog

        ghost = Entity(animanager=self.animanagers['ghost'], speed=10, max_health=100, strength=10,
                       vision_area=Vector2D(self.cam.frame.width, self.cam.frame.height), family='ghost')
        ghost.immortal = False
        self.examples['ghost'] = ghost

        demon = Entity(animanager=self.animanagers['demon'], speed=12, max_health=200, strength=40,
                       vision_area=Vector2D(self.cam.frame.width, self.cam.frame.height), family='demon')
        self.examples['demon'] = demon

        hell_beast = Entity(animanager=self.animanagers['hell-beast'], speed=20, max_health=300,
                            strength=100, vision_area=Vector2D(self.cam.frame.width, self.cam.frame.height), family='hell-beast')
        hell_beast.friends.append('hell-beast')
        hell_beast.friends.append('hero')
        self.examples['hell-beast'] = hell_beast

        for example in self.examples.values():
            if example.container == 'entity':
                example.generate_random_priorities(env_states=self.game_env.get_states())

        self.evolution.add_example(EvolutionExample(self.examples['hell-beast'], min_=2, max_=2,
                                                                  area=self.game_world.get_area()))
                                   #start_genome_file=self.genomes_files['genome1'])

        #self.evolution.add_example('ghost', EvolutionExample(self.examples['ghost'], min_=2, max_=20,
                                                             #area=self.game_world.get_area()))
        self.spawn.add_example(SpawnExample(self.examples['ghost'], min_=2, max_=2, duration=1000,
                                                     area=self.game_world.get_area(), shift=Vector2D(10, 10)))

        self.spawn.add_example(SpawnExample(self.examples['tree'], min_=10, max_=50, duration=100000,
                                            area=self.game_world.get_area(), shift=Vector2D(10, 10)))

    def add_decorations(self):
        self.spawn.spawn_rect(rect=self.game_world.get_area(),
                              obj=self.examples['immortal-tree'], shift=Vector2D(10, 10))

        #self.spawn.spawn_random(count=50, area=self.game_world.get_area(),
                               #obj=self.examples['tree'], shift=Vector2D(15, 15))

        self.tree_start = len(self.decorations)
        self.tree_count = self.tree_start

        '''
        self.spawn.spawn_random(container_name='decorations', count=30, area=self.game_world.get_area(),
                                obj=self.examples['tree-dried'], shift=Vector2D(15, 15))
        self.spawn.spawn_random(container_name='decorations', count=10, area=self.game_world.get_area(),
                                obj=self.examples['monument'], shift=Vector2D(15, 15))
        '''

    def add_entities(self):
        self.hero = self.spawn.spawn(obj=self.examples['hero'], return_obj=True)
        #self.spawn.spawn_random(count=5, area=self.game_world.get_area(),
                                #obj=self.examples['dog'], shift=Vector2D(15, 15))

    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(self.fps)
            time = clock.get_time()
            time = time / 80  # game speed

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
        for ent in self.entities:
            # Vision
            rect = ent.get_rect()
            area = Rect(rect.center.x, rect.center.y,
                        ent.vision_area.x, ent.vision_area.y, isCenter=True)
            entities_around = [_ for _ in self.entities if _.alive and _.get_rect().intersects(area) and _ is not ent]
            decorations_around = [_ for _ in self.decorations if _.get_rect().intersects(area)]
            #objects_around = entities_around + decorations_around
            #world_around = self.game_world.get_world_around(ent.get_rect().center)
            #self.game_env.apply(entity=ent, objects_around=objects_around)

            # Controlling
            if not ent.ai:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    exit(0)
                if keys[pygame.K_BACKSPACE]:
                    self.allow_draw = not self.allow_draw
                ent.control(keys, time, entities_around, decorations_around)
            else:
                ent.ai_control(time, entities_around, decorations_around)

    def update(self, time):
        for dec in self.decorations:
            dec.update(time)
            if not dec.alive:
                self.spawn.safe_remove(dec)

        for ent in self.entities:
            ent.update(time)
            if not ent.alive:
                if ent.ai:
                    self.evolution.archive(ent.family)
                    self.spawn.safe_remove(ent)
                else:
                    print('You are dead')
                    exit(1)

        self.evolution.update()
        self.spawn.update()
        self.cam.update(self.hero.get_rect().center)
        self.sun.update(time)
        pygame.display.update()

    def draw(self):
        self.canvas.fill((0, 0, 0))  # Makes black window

        self.game_world.draw(surface=self.canvas, position=self.hero.get_rect().center, camera=self.cam)
        objects = self.decorations + self.entities
        objects.sort(key=lambda obj: obj.get_rect().bottom)  # sorting objects by y axis
        for obj in objects:
            if obj.get_rect().intersects(self.cam.frame):
                obj.draw(self.canvas, self.cam.get_scroll())

        #self.canvas.blit(self.sun.img, (self.cam.frame.topleft.x + self.cam.get_scroll().x,
                                        #self.cam.frame.topleft.y + self.cam.get_scroll().y))

        self.window.blit(pygame.transform.scale(self.canvas, [self.screen_size.x * self.cam.coefficient,
                                                              self.screen_size.y * self.cam.coefficient]),
                         (-self.cam.frame.width, -self.cam.frame.height))

if __name__ == '__main__':
    game = Game(Vector2D(1280, 720), 'Multiverse')
    game.run()