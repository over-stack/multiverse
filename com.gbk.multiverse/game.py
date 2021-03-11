import numpy as np
import pygame

from camera import Camera
from animationManager import AnimationManager
from world import World
from entity import Entity
from decoration import Decoration
from environment import Environment
#from sun import Sun
from spawn import Spawn, SpawnExample
from evolution import Evolution, EvolutionExample
from genome import Genome
from item import Food

from my_libs import Rect, Vector2D, InterManager
from thread_system import VCIThread

from time import monotonic

# add function add_friend()
# add debug container for drawing
# shift in spawn = border
# refactor spawn
# make families instead of example_name
# beautiful features writing
# add function scale to rectangle
# add switching between different ai algorithms
# add map limits for moving   (with accurate camera rendering)
# add fps counter
# add acceleration
# optimize loops
# clear imports
# add simple rendering (learn mode)
# path finding algorithm
# make conditions to genetic alg

# fix random bag with map
# fix animationManager

# add spawn_rect by count
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

import os
import platform


class Game:
    def __init__(self, screen_size, title):
        #if platform.system() == 'Windows':
            #os.environ['SDL_VIDEODRIVER'] = 'windib'
        #os.environ['SDL_VIDEODRIVER'] = 'dummy'

        self.screen_size = screen_size
        self.title = title
        self.fps = 200

        pygame.init()
        print(pygame.display.list_modes())
        print(pygame.display.get_driver())
        self.window = pygame.display.set_mode(screen_size.get_tuple(),
                                              pygame.HWSURFACE | pygame.DOUBLEBUF)  # only for draw the canvas | pygame.OPENGL
        self.canvas = self.window.copy()  # used to draw

        pygame.display.set_caption(title)
        #pygame.event.set_allowed([pygame.QUIT, pKEYDOWN, KEYUP])

        self.hero = None

        self.resources = dict()
        self.sheets = dict()
        self.animanagers = dict()
        self.examples = dict()
        self.decorations = list()
        self.entities = list()
        self.items = list()
        self.genomes_files = dict()

        self.font = pygame.font.Font(None, 30)

        self.sum_time = {'VCI': 0, 'Update': 0, 'Draw': 0}
        self.N = 0
        self.frame_mod = 2
        self.frame = 0
        self.num_threads = 4

        self.frames = 0
        self.seconds = monotonic()

        self.cam = Camera(screen_size=self.screen_size, coefficient=1)

        self.include_resources()
        self.animation_managers()

        self.spawn = Spawn({'decorations': self.decorations, 'entities': self.entities, 'items': self.items})
        self.evolution = Evolution(self.spawn)
        #self.game_env = Environment()
        self.game_world = World(filename=f'{self.resources["tiny-rpg"]}tileset.png', size=Vector2D(1400, 1400),
                                tile_size=Vector2D(16, 16))
        self.game_world.load_map(self.game_world.generate_world())
        #self.sun = Sun(self.cam.frame.width, self.cam.frame.height)

        self.add_examples()
        #self.encoder = Encoder(self.game_world.tile_size, Vector2D(self.cam.frame.width, self.cam.frame.height),
                               #self.examples.values(), self.game_world.get_codes())

        self.add_decorations()
        self.add_entities()
        self.add_items()

        self.allow_draw = True
        self.tree_count = 0  #######################
        self.tree_start = 0

        self.train = list()

        self.inter_manager = InterManager()

        self.global_time = 0  # / 80

    def include_resources(self):
        self.resources['goth'] = 'resources/gothicvania patreon collection/'
        self.resources['tiny-rpg'] = 'resources/tiny-RPG-forest-files/PNG/environment/'

        self.sheets['bush'] = dict()
        self.sheets['bush']['stay'] = pygame.transform.scale2x(pygame.image.load(f'{self.resources["tiny-rpg"]}/sliced-objects/bush.png').convert_alpha())

        self.sheets['tree'] = dict()
        self.sheets['tree']['stay'] = pygame.transform.scale2x(pygame.image.load(f'{self.resources["tiny-rpg"]}/sliced-objects/tree-pink.png').convert_alpha())

        self.sheets['tree-dried'] = dict()
        self.sheets['tree-dried']['stay'] = pygame.transform.scale2x(pygame.image.load(f'{self.resources["tiny-rpg"]}/sliced-objects/tree-dried.png').convert_alpha())

        self.sheets['monument'] = dict()
        self.sheets['monument']['stay'] = pygame.transform.scale2x(pygame.image.load(f'{self.resources["tiny-rpg"]}/sliced-objects/rock-monument.png').convert_alpha())

        self.sheets['fence_v'] = dict()
        self.sheets['fence_v']['stay'] = pygame.transform.scale2x(
            pygame.image.load(f'{self.resources["tiny-rpg"]}/fence_v.png').convert_alpha())

        self.sheets['fence_hl'] = dict()
        self.sheets['fence_hl']['stay'] = pygame.transform.scale2x(
            pygame.image.load(f'{self.resources["tiny-rpg"]}/fence_hl.png').convert_alpha())

        self.sheets['hero'] = dict()
        self.sheets['hero']['stay'] = pygame.transform.scale2x(pygame.image.load(
            f'{self.resources["goth"]}Gothic-hero-Files/PNG/gothic-hero-idle.png').convert_alpha())
        self.sheets['hero']['attack'] = pygame.transform.scale2x(pygame.image.load(
            f'{self.resources["goth"]}Gothic-hero-Files/PNG/gothic-hero-attack.png').convert_alpha())
        self.sheets['hero']['run'] = pygame.transform.scale2x(pygame.image.load(
            f'{self.resources["goth"]}Gothic-hero-Files/PNG/gothic-hero-run.png').convert_alpha())

        self.sheets['ghost'] = dict()
        self.sheets['ghost']['stay'] = pygame.transform.scale2x(pygame.image.load(f'{self.resources["goth"]}Ghost-Files/PNG/ghost-idle.png').convert_alpha())
        self.sheets['ghost']['walk'] = pygame.transform.scale2x(pygame.image.load(f'{self.resources["goth"]}Ghost-Files/PNG/ghost-shriek.png').convert_alpha())
        self.sheets['ghost']['death'] = pygame.transform.scale2x(pygame.image.load(f'{self.resources["goth"]}Ghost-Files/PNG/ghost-vanish.png').convert_alpha())

        self.sheets['dog'] = dict()
        self.sheets['dog']['stay'] = pygame.transform.scale2x(pygame.image.load(
            f'{self.resources["goth"]}Hell-Hound-Files/PNG/hell-hound-idle.png').convert_alpha())
        self.sheets['dog']['walk'] = pygame.transform.scale2x(pygame.image.load(
            f'{self.resources["goth"]}Hell-Hound-Files/PNG/hell-hound-walk.png').convert_alpha())

        self.sheets['demon'] = dict()
        self.sheets['demon']['stay'] = pygame.transform.scale2x(pygame.image.load(
            f'{self.resources["goth"]}demon-Files/PNG/demon-idle.png').convert_alpha())
        self.sheets['demon']['attack'] = pygame.transform.scale2x(pygame.image.load(
            f'{self.resources["goth"]}demon-Files/PNG/demon-attack.png').convert_alpha())

        self.sheets['hell-beast'] = dict()
        self.sheets['hell-beast']['stay'] = pygame.transform.scale2x(pygame.image.load(
            f'{self.resources["goth"]}Hell-Beast-Files/PNG/with-stroke/hell-beast-idle.png').convert_alpha())
        self.sheets['hell-beast']['attack'] = pygame.transform.scale2x(pygame.image.load(
            f'{self.resources["goth"]}Hell-Beast-Files/PNG/with-stroke/hell-beast-breath.png').convert_alpha())

        self.genomes_files['genome1'] = 'neural_network/weights/weights.npy'

    def animation_managers(self):
        self.animanagers['bush'] = AnimationManager(collision_rect=Rect(0, 0, 58, 48))
        self.animanagers['bush'].create(name='stay', sheet=self.sheets['bush']['stay'],
                                        cols=1, rows=1, count=1, speed=0)

        self.animanagers['tree'] = AnimationManager(collision_rect=Rect(0, 0, 120, 140))
        self.animanagers['tree'].create(name='stay', sheet=self.sheets['tree']['stay'],
                                        cols=1, rows=1, count=1, speed=0)

        self.animanagers['tree-dried'] = AnimationManager()
        self.animanagers['tree-dried'].create(name='stay', sheet=self.sheets['tree-dried']['stay'],
                                        cols=1, rows=1, count=1, speed=0)

        self.animanagers['fence_v'] = AnimationManager(collision_rect=Rect(0, 0, 120, 42))
        self.animanagers['fence_v'].create(name='stay', sheet=self.sheets['fence_v']['stay'],
                                              cols=1, rows=1, count=1, speed=0)

        self.animanagers['fence_hl'] = AnimationManager(collision_rect=Rect(0, 0, 42, 120))
        self.animanagers['fence_hl'].create(name='stay', sheet=self.sheets['fence_hl']['stay'],
                                           cols=1, rows=1, count=1, speed=0)

        self.animanagers['monument'] = AnimationManager()
        self.animanagers['monument'].create(name='stay', sheet=self.sheets['monument']['stay'],
                                        cols=1, rows=1, count=1, speed=0)

        self.animanagers['hero'] = AnimationManager(collision_rect=Rect(0, 0, 76, 96))
        self.animanagers['hero'].create(name='stay', sheet=self.sheets['hero']['stay'],
                                        cols=4, rows=1, count=4, speed=0.2, looped=True)
        self.animanagers['hero'].create(name='attack', sheet=self.sheets['hero']['attack'],
                                        cols=6, rows=1, count=6, speed=0.9)
        self.animanagers['hero'].create(name='walk', sheet=self.sheets['hero']['run'],
                                        cols=12, rows=1, count=12, speed=0.9, looped=True)

        self.animanagers['ghost'] = AnimationManager(collision_rect=Rect(0, 0, 50, 50), defaultFlipped=True)
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
        hero = Entity(animanager=self.animanagers['hero'], speed=10, max_health=800,
                      strength=100, vision_area=Vector2D(self.cam.frame.width, self.cam.frame.height),
                      family='hero')  # family=hero -> main character
        hero.ai = False
        #hero.immortal = True
        hero.strength = 30
        hero.position = Vector2D(300, 300)
        hero.alive = True
        hero.friends.append('ghost')
        hero.friendly_collision = False
        #hero.isCollision = True
        #hero.satiety_speed = 0
        #hero.friends.append('hell-beast')
        #hero.make_ghost()
        self.examples['hero'] = hero

        bush = Food(self.animanagers['bush'], 100)
        self.examples['bush'] = bush
        self.examples['bush_l'] = bush.copy()
        self.examples['bush_l'].family = 'bush_l'
        self.examples['bush_r'] = bush.copy()
        self.examples['bush_r'].family = 'bush_r'
        self.examples['bush_t'] = bush.copy()
        self.examples['bush_t'].family = 'bush_t'
        self.examples['bush_b'] = bush.copy()
        self.examples['bush_b'].family = 'bush_b'

        tree = Decoration(animanager=self.animanagers['tree'], max_health=1000, family='tree')
        self.examples['tree'] = tree

        tree_dried = Decoration(animanager=self.animanagers['tree-dried'], max_health=1000, family='tree-dried')
        self.examples['tree-dried'] = tree_dried

        immortal_tree = Decoration(animanager=self.animanagers['tree'], max_health=1000, family='immortal-tree')
        immortal_tree.immortal = True
        self.examples['immortal-tree'] = immortal_tree

        monument = Decoration(animanager=self.animanagers['monument'], max_health=5000, family='monument')
        self.examples['monument'] = monument

        fence_v = Decoration(animanager=self.animanagers['fence_v'], max_health=5000, family='fence')
        fence_v.immortal = True
        self.examples['fence_v'] = fence_v

        fence_hl = Decoration(animanager=self.animanagers['fence_hl'], max_health=5000, family='fence')
        fence_hl.immortal = True
        self.examples['fence_hl'] = fence_hl

        dog = Entity(animanager=self.animanagers['dog'], speed=-12, max_health=80, strength=14,
                     vision_area=Vector2D(self.cam.frame.width, self.cam.frame.height), family='dog')
        self.examples['dog'] = dog

        ghost = Entity(animanager=self.animanagers['ghost'], speed=20, max_health=100, strength=40,
                       vision_area=Vector2D(self.cam.frame.width, self.cam.frame.height), family='ghost')
        ghost.friends.append('ghost')
        ghost.friends.append('hero')
        ghost.friendly_collision = False
        #ghost.friends.append('hero')
        #ghost.animanager.simple_drawing = True
        ghost.genome.load('neural_network/weights/weightsNN.npy')
        self.examples['ghost'] = ghost

        demon = Entity(animanager=self.animanagers['demon'], speed=12, max_health=200, strength=200,
                       vision_area=Vector2D(self.cam.frame.width, self.cam.frame.height), family='demon')
        demon.ai_custom = False
        self.examples['demon'] = demon

        hell_beast = Entity(animanager=self.animanagers['hell-beast'], speed=20, max_health=400,
                            strength=100, vision_area=Vector2D(self.cam.frame.width, self.cam.frame.height), family='hell-beast')
        hell_beast.friends.append('hell-beast')
        #hell_beast.friends.append('hero')
        hell_beast.friendly_collision = False
        hell_beast.ai_custom = False
        #hell_beast.friends.append('hero')
        self.examples['hell-beast'] = hell_beast

        for example in self.examples.values():
            if example.container == 'entity':
                example.generate_random_priorities(env_states=self.game_env.get_states())

       # self.evolution.add_example(EvolutionExample(self.examples['hell-beast'], min_=1, max_=4,
                                                    #area=self.game_world.get_area()))
                                   #start_genome_file='neural_network/weights/weightsNN.npy')

        self.evolution.add_example(EvolutionExample(self.examples['ghost'], min_=10, max_=60,
                                                    area=self.game_world.get_area(shift=600)))
        self.spawn.add_example(SpawnExample(self.examples['bush_l'], min_=1, max_=8, duration=120,
                                            area=Rect(150, 150, 200, 1350), shift=Vector2D(10, 10)))
        self.spawn.add_example(SpawnExample(self.examples['bush_r'], min_=1, max_=8, duration=120,
                                            area=Rect(950, 150, 200, 1350), shift=Vector2D(10, 10)))
        self.spawn.add_example(SpawnExample(self.examples['bush_t'], min_=1, max_=8, duration=120,
                                            area=Rect(350, 150, 600, 200), shift=Vector2D(10, 10)))
        self.spawn.add_example(SpawnExample(self.examples['bush_b'], min_=1, max_=8, duration=120,
                                            area=Rect(350, 950, 600, 200), shift=Vector2D(10, 10)))
        #self.spawn.add_example(SpawnExample(self.examples['ghost'], min_=2, max_=5, duration=30,
                                            #area=self.game_world.get_area(), shift=Vector2D(10, 10)))

        #self.spawn.add_example(SpawnExample(self.examples['tree'], min_=10, max_=10, duration=100000,
                                            #area=self.game_world.get_area(), shift=Vector2D(10, 10)))

    def add_decorations(self):
        self.spawn.spawn_rect(rect=self.game_world.get_area(), obj=self.examples['immortal-tree'], shift=Vector2D(0, 0))

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
                                #obj=self.examples['ghost'], shift=Vector2D(15, 15))

    def add_items(self):
        pass
        #self.spawn.spawn_random(count=20, area=self.game_world.get_area(),
                                #obj=self.examples['bush'], shift=Vector2D(15, 15))

    def run(self):
        #self.inter_manager.make_decorations_table(self.entities, self.decorations)
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(0)
            time = clock.get_time()
            time = time / 80  # game speed
            self.global_time += time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.spawn.safe_spawn(self.examples['bush'], position=self.hero.position)

            self.vci(time)
            self.update(time)

            if self.allow_draw:
                self.draw()

            self.N += 1
            self.frame += 1
            if self.frame >= self.frame_mod:
                self.frame = 0

            self.frames += 1

            #print('FPS:', self.frames // (monotonic() - self.seconds))
            #print('VCI:', self.sum_time['VCI']/self.N)
            #print('Update:', self.sum_time['Update'] / self.N)
            #print('Draw:', self.sum_time['Draw'] / self.N)
            #print('Count of objects:', len(self.decorations) + len(self.entities))
            #print('Time:', time)

            #print(self.global_time)
            #print('-------------------------------------')

        pygame.quit()

    # vision controlling and interaction
    def vci(self, time):
        start = monotonic()

        #self.inter_manager.tick(time)
        #self.inter_manager.make_entities_table(self.entities)

        '''
        threads = list()
        for i in range(self.num_threads):
            count = len(self.entities) // self.num_threads
            threads.append(VCIThread(self.inter_manager.table, self.entities, time,
                                     range(i * count, (i+1) * count),
                                     self.frame_mod, self.frame))
            threads[i].start()
        '''


        sum_ = 0

        for i in range(len(self.entities)):
            # Vision
            ent = self.entities[i]
            if True:
                area = Rect(ent.get_rect().center.x, ent.get_rect().center.y,
                            self.cam.frame.width, self.cam.frame.height, isCenter=True)
                entities_around = [_ for _ in self.entities if
                                   _.alive and _.get_rect().intersects(area) and _ is not ent]
                decorations_around = [_ for _ in self.decorations if _.get_rect().intersects(area)]
                items_around = [_ for _ in self.items if _.get_rect().intersects(area)]

                #entities_around = self.inter_manager.ent_table[ent]
                #decorations_around = self.inter_manager.get_decorations_around(ent)

                #if ent == self.hero:
                    #print(decorations_around)
                #objects_around = entities_around + decorations_around
                #world_around = self.game_world.get_world_around(ent.get_rect().center)
                #self.game_env.apply(entity=ent, objects_around=objects_around)


                if ent.ai:
                    #start = monotonic()
                    ent.control(time, entities_around, decorations_around, items_around, i % self.frame_mod != self.frame)
                    #end = monotonic()
                    #sum_ += end - start
                else:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_ESCAPE]:
                        exit(0)
                    if keys[pygame.K_BACKSPACE]:
                        self.allow_draw = not self.allow_draw
                    ent.control(time, entities_around, decorations_around, items_around, keys, i % self.frame_mod != self.frame)


        '''
        entities_around = self.inter_manager.table[self.hero]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit(0)
        if keys[pygame.K_BACKSPACE]:
            self.allow_draw = not self.allow_draw
        self.hero.control(time, entities_around, [], keys)


        for thread in threads:
            thread.join()
        '''

        end = monotonic()
        sum_ = end - start
        self.sum_time['VCI'] += sum_

    def update(self, time):
        start = monotonic()
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

        for item in self.items:
            if not item.dropped:
                self.spawn.safe_remove(item)

        self.evolution.update()
        self.spawn.update()
        self.cam.update(self.hero.get_rect().center)
        #self.inter_manager.update()
        #self.sun.update(time)
        pygame.display.update()
        end = monotonic()
        self.sum_time['Update'] += end - start

    def draw(self):
        start = monotonic()
        self.canvas.fill((0, 0, 0))  # Makes black window

        self.game_world.draw(surface=self.canvas, position=self.hero.get_rect().center, camera=self.cam)
        objects = self.decorations + self.entities + self.items
        objects.sort(key=lambda obj: obj.get_rect().bottom)  # sorting objects by y axis
        for obj in objects:
            if obj.get_rect().intersects(self.cam.frame):
                obj.draw(self.canvas, self.cam.get_scroll())

        #self.canvas.blit(self.sun.img, (self.cam.frame.topleft.x + self.cam.get_scroll().x,
                                        #self.cam.frame.topleft.y + self.cam.get_scroll().y))

        #self.window.blit(pygame.transform.scale(self.canvas, [self.screen_size.x * self.cam.coefficient,
                                                              #self.screen_size.y * self.cam.coefficient]),
                         #(-self.cam.frame.width, -self.cam.frame.height))

        self.window.blit(self.canvas, (0, 0))
        end = monotonic()
        self.sum_time['Draw'] += end - start


if __name__ == '__main__':
    game = Game(Vector2D(1280, 720), 'Multiverse')
    game.run()