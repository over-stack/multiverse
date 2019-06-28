import numpy as np
import pygame

from animationManager import AnimationManager
from entity import Entity
from world import World
from camera import Camera
from decoration import Decoration
from environment import Environment

from evolution import EvolutionAlg

class Game:

    def __init__(self, screen_size, title):
        self.screen_size = screen_size
        self.title = title

        pygame.init()
        self.window = pygame.display.set_mode(screen_size, pygame.HWSURFACE|pygame.DOUBLEBUF)
        self.canvas = self.window.copy()

        pygame.display.set_caption(title)

        self.fps = 60

        self.decorations = list()
        self.entities = list()
        self.free_id = 0

    def include_resources(self):

        self.resources_dir = 'resources/gothicvania patreon collection/'
        self.resources_dir1 = 'resources/tiny-RPG-forest-files/PNG/environment/'

        self.tree_sheet_stay = pygame.image.load(self.resources_dir1 + '/sliced-objects/tree-pink.png')

        self.hero_sheet_stay = pygame.image.load(self.resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-idle.png')
        self.hero_sheet_attack = pygame.image.load(self.resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-attack.png')
        self.hero_sheet_run = pygame.image.load(self.resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-run.png')

        self.ghost_sheet_stay = pygame.image.load(self.resources_dir + 'Ghost-Files/PNG/ghost-idle.png')
        self.ghost_sheet_walk = pygame.image.load(self.resources_dir + 'Ghost-Files/PNG/ghost-shriek.png')
        self.ghost_sheet_death = pygame.image.load(self.resources_dir + 'Ghost-Files/PNG/ghost-vanish.png')

        self.dog_sheet_stay = pygame.image.load(self.resources_dir + 'Hell-Hound-Files/PNG/hell-hound-idle.png')
        self.dog_sheet_walk = pygame.image.load(self.resources_dir + 'Hell-Hound-Files/PNG/hell-hound-walk.png')

        self.animation_managers()

    def animation_managers(self):

        self.anim_dec = AnimationManager()
        self.anim_hero = AnimationManager()
        self.anim_dog = AnimationManager()
        self.anim_ghost = AnimationManager()

        self.anim_dec.create(name='stay', sheet=self.tree_sheet_stay,
                             cols=1, rows=1, count=1, speed=0)

        self.anim_hero.create(name='stay', sheet=self.hero_sheet_stay,
                              cols=4, rows=1, count=4, speed=0.2, looped=True)
        self.anim_hero.create(name='attack', sheet=self.hero_sheet_attack,
                              cols=6, rows=1, count=6, speed=0.9)
        self.anim_hero.create(name='walk', sheet=self.hero_sheet_run,
                              cols=12, rows=1, count=12, speed=0.9, looped=True)

        self.anim_ghost.create(name='stay', sheet=self.ghost_sheet_stay,
                               cols=7, rows=1, count=7, speed=0.5, looped=True)
        self.anim_ghost.create(name='attack', sheet=self.ghost_sheet_walk,
                               cols=4, rows=1, count=4, speed=0.5, looped=False)
        self.anim_ghost.create(name='death', sheet=self.ghost_sheet_death,
                               cols=7, rows=1, count=7, speed=0.5, looped=False)

        self.anim_dog.create(name='stay', sheet=self.dog_sheet_stay,
                             cols=6, rows=1, count=6, speed=0.5, looped=True)
        self.anim_dog.create(name='walk', sheet=self.dog_sheet_walk,
                             cols=12, rows=1, count=12, speed=0.5, looped=True)

    def new(self):

        self.cam = Camera(screen_size=self.screen_size, coef=2)

        self.inc_world = self.world_settings()
        self.inc_environment = self.environment_settings()

        self.inc_decorations = self.add_decorations()
        self.inc_entities = self.add_entities()

        self.sun = pygame.Surface((self.cam.width, self.cam.height))
        self.sun.fill((0, 0, 0))
        self.sun_brightness = 255

    def world_settings(self):
        self.game_world = World(filename=self.resources_dir1 + 'tileset.png', size=(2000, 2000), tile_size=(16, 16))
        self.game_world.add_tile(position=(208, 288), code=0)

        return True

    def environment_settings(self):
        bonus = dict()
        bonus['forest'] = {'health': 15, 'strength': 10, 'satiety': 20}  # in percents
        bonus['alone'] = {'health': 8, 'strength': 15, 'satiety': 25}
        bonus['support'] = {'health': 15, 'strength': 10, 'satiety': 20}

        conditions = dict()
        conditions['forest'] = ['family', 'tree', '>', '4']
        conditions['alone'] = ['type', 'entity', '==', '0']
        conditions['support'] = ['family', 'same', '>', '3']

        self.game_env = Environment(bonus=bonus, conditions=conditions)

        return True

    def add_decorations(self):
        random_positions = np.random.rand(20, 2) * 1000

        for i in range(20):
            self.decorations.append(Decoration(animanager=self.anim_dec.copy(),
                                               position=list(random_positions[i, :]),
                                               max_health=1000, id_=self.free_id, family='tree'))
            self.free_id += 1

        return True

    def add_entities(self):
        self.hero = Entity(animanager=self.anim_hero.copy(), position=[800, 400], speed=10, max_health=200,
                           strength=20, id_=self.free_id, family='hero')
        self.hero.ai = False
        self.entities.append(self.hero)
        self.free_id += 1

        dog = Entity(animanager=self.anim_dog.copy(), position=[1100, 450], speed=-12, max_health=80,
                     strength=14, id_=self.free_id, family='dog')
        dog.acceleration[0] = dog.speed / 2

        self.entities.append(dog)
        self.free_id += 1

        random_positions = np.random.rand(10, 2) * 1000

        for i in range(1):
            self.entities.append(Entity(animanager=self.anim_ghost.copy(), position=list(random_positions[i, :]),
                                        speed=10, max_health=200, strength=20, id_=self.free_id,
                                        family='ghost'))
            self.entities[-1].id_ = self.free_id
            self.free_id += 1

        if self.inc_environment:
            for ent in self.entities:
                ent.generate_priorities(env_states=self.game_env.get_states())

        return True

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

            keys = pygame.key.get_pressed()

            self.vci(keys)  # vision controlling and interaction

            self.update(time)

            self.sun_brightness -= 0.1

            self.draw()

        pygame.quit()

    def vci(self, keys):
        for ent in self.entities:
            # Vision
            area = [ent.position[0] - self.cam.width / 2,
                    ent.position[1] - self.cam.height / 2,
                    self.cam.width, self.cam.height]

            entities_around = [_ for _ in self.entities if _.in_area(area) and not _ is ent]

            decorations_around = [_ for _ in self.decorations if _.in_area(area)]

            objects_around = entities_around + decorations_around

            ent.look_around(objects_around=objects_around,
                            world_around=self.game_world.get_world_around(ent.position))

            # Controlling
            if not ent.ai:
                ent.control(keys)

            ent.check_collision(self.entities + self.decorations)

    def update(self, time):

        for dec in self.decorations:
            dec.update(time)

            if dec.health <= 0:
                self.decorations.remove(dec)

        for ent in self.entities:
            ent.update(time)

            if not ent.alive:
                self.entities.remove(ent)

                if not ent.ai:
                    print('You are dead')
                    exit(1)

            self.game_env.apply(entity=ent, objects_around=ent.objects_around,
                                world_around=self.game_world.get_world_around(ent.position))

        self.cam.update(self.hero.position)
        pygame.display.update()

    def draw(self):

        self.window.fill((0, 0, 0))  # Makes black window
        self.canvas.fill((0, 0, 0))

        objects = self.decorations + self.entities

        objects.sort(key=lambda obj: obj.position[1])  # sorting objects by y axis  # + obj.height

        self.game_world.draw(surface=self.canvas, scroll=self.cam.frame, position=self.hero.position,
                             width=self.cam.width / 2 + self.cam.bias,
                             height=self.cam.height / 2 + self.cam.bias)  # draw map

        draw_area = [self.hero.position[0] - self.cam.width / 2 - self.cam.bias,  # bias needs to draw
                     self.hero.position[1] - self.cam.height / 2 - self.cam.bias,
                     self.cam.width + self.cam.bias, self.cam.height + self.cam.bias]

        for obj in objects:
            if obj.in_area(draw_area):
                obj.draw(self.canvas, self.cam.frame)

        self.sun.set_alpha(255 - self.sun_brightness)
        self.canvas.blit(self.sun, (self.hero.position[0] - self.cam.width / 2 + self.cam.frame[0],
                                    self.hero.position[1] - self.cam.height / 2 + self.cam.frame[1]))

        self.window.blit(pygame.transform.scale(self.canvas, [self.screen_size[0] * self.cam.coef,
                                                              self.screen_size[1] * self.cam.coef]),
                         (-self.cam.width, -self.cam.height))

if __name__ == '__main__':
    game = Game([1280, 720], 'Multiverse')

    game.include_resources()
    game.new()
    game.run()