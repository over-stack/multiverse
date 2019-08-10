import numpy as np
import pygame

from animationManager import AnimationManager
from entity import Entity
from world import World
from camera import Camera
from decoration import Decoration
from environment import Environment
from sun import Sun

from evolution import EvolutionAlg

from my_libs import Rect, Vector2D

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

    def include_resources(self):
        self.res_dirs = ('resources/gothicvania patreon collection/',
                         'resources/tiny-RPG-forest-files/PNG/environment/')

        self.tree_sheet_stay = pygame.image.load(f'{self.res_dirs[1]}/sliced-objects/tree-pink.png')

        self.hero_sheet_stay = pygame.image.load(f'{self.res_dirs[0]}Gothic-hero-Files/PNG/gothic-hero-idle.png')
        self.hero_sheet_attack = pygame.image.load(f'{self.res_dirs[0]}Gothic-hero-Files/PNG/gothic-hero-attack.png')
        self.hero_sheet_run = pygame.image.load(f'{self.res_dirs[0]}Gothic-hero-Files/PNG/gothic-hero-run.png')

        self.ghost_sheet_stay = pygame.image.load(f'{self.res_dirs[0]}Ghost-Files/PNG/ghost-idle.png')
        self.ghost_sheet_walk = pygame.image.load(f'{self.res_dirs[0]}Ghost-Files/PNG/ghost-shriek.png')
        self.ghost_sheet_death = pygame.image.load(f'{self.res_dirs[0]}Ghost-Files/PNG/ghost-vanish.png')

        self.dog_sheet_stay = pygame.image.load(f'{self.res_dirs[0]}Hell-Hound-Files/PNG/hell-hound-idle.png')
        self.dog_sheet_walk = pygame.image.load(f'{self.res_dirs[0]}Hell-Hound-Files/PNG/hell-hound-walk.png')

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
        self.cam = Camera(screen_size=self.screen_size, coefficient=2)

        self.sun = Sun(self.cam.frame.width, self.cam.frame.height)

        self.decorations = list()
        self.entities = list()
        self.free_id = 0

        self.environment_settings()
        self.world_settings()
        self.add_decorations()
        self.add_entities()

    def environment_settings(self):
        self.game_env = Environment()

    def world_settings(self):
        self.game_world = World(filename=f'{self.res_dirs[1]}tileset.png', size=Vector2D(2000, 2000),
                                tile_size=Vector2D(16, 16))
        self.game_world.add_tile(position=Vector2D(208, 288), code=0)

    def add_decorations(self):
        random_positions = np.random.rand(20, 2) * 1000
        for i in range(20):
            self.decorations.append(Decoration(animanager=self.anim_dec.copy(),
                                               position=Vector2D(random_positions[i, 0], random_positions[i, 1]),
                                               max_health=1000, id_=self.free_id, family='tree'))
            self.free_id += 1

        return True

    def add_entities(self):
        self.hero = Entity(animanager=self.anim_hero.copy(), position=Vector2D(0, 0), speed=10, max_health=200,
                           strength=20, id_=self.free_id, family='hero')
        self.hero.ai = False
        self.entities.append(self.hero)
        self.free_id += 1

        dog = Entity(animanager=self.anim_dog.copy(), position=Vector2D(1100, 450), speed=-12, max_health=80,
                     strength=14, id_=self.free_id, family='dog')
        dog.acceleration.x = dog.speed / 2
        self.entities.append(dog)
        self.free_id += 1

        random_positions = np.random.rand(10, 2) * 1000
        for i in range(1):
            self.entities.append(Entity(animanager=self.anim_ghost.copy(),
                                        position=Vector2D(random_positions[i, 0], random_positions[i, 1]),
                                        speed=10, max_health=200, strength=20, id_=self.free_id,
                                        family='ghost'))
            self.entities[-1].id_ = self.free_id
            self.free_id += 1

        for ent in self.entities:
            ent.generate_random_priorities(env_states=self.game_env.get_states())

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

            self.draw()

        pygame.quit()

    def vci(self, keys):
        for ent in self.entities:
            # Vision
            area = Rect(ent.get_rect().left - self.cam.frame.width / 2,
                        ent.get_rect().top - self.cam.frame.height / 2,
                        self.cam.frame.width, self.cam.frame.height)

            entities_around = [_ for _ in self.entities if _.get_rect().intersects(area) and not _ is ent]
            decorations_around = [_ for _ in self.decorations if _.get_rect().intersects(area)]
            objects_around = entities_around + decorations_around

            self.game_env.apply(entity=ent, objects_around=objects_around,
                                world_around=self.game_world.get_world_around(Vector2D(ent.get_rect().center.x,
                                                                                       ent.get_rect().center.y)))

            # Controlling
            if not ent.ai:
                ent.control(keys)
            ent.collision(self.entities + self.decorations)
            ent.interaction(objects_around)

    def update(self, time):
        self.sun.update(time)

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

        self.cam.update(Vector2D(self.hero.get_rect().center.x, self.hero.get_rect().center.y))
        pygame.display.update()

    def draw(self):
        self.canvas.fill((0, 0, 0))  # Makes black window

        objects = self.decorations + self.entities

        objects.sort(key=lambda obj: obj.get_rect().top)  # sorting objects by y axis  # + obj.height

        self.game_world.draw(surface=self.canvas, scroll=Vector2D(self.cam.frame.left, self.cam.frame.top),
                             position=Vector2D(self.hero.get_rect().left, self.hero.get_rect().top),
                             width=self.cam.frame.width / 2 + self.cam.bias,
                             height=self.cam.frame.height / 2 + self.cam.bias)  # draw map

        draw_area = Rect(self.hero.get_rect().center.x - self.cam.frame.width / 2 - self.cam.bias,  # bias needs to draw
                         self.hero.get_rect().center.y - self.cam.frame.height / 2 - self.cam.bias,
                         self.cam.frame.width + self.cam.bias, self.cam.frame.height + self.cam.bias)

        for obj in objects:
            if obj.get_rect().intersects(draw_area):
                obj.draw(self.canvas, self.cam.frame)

        self.canvas.blit(self.sun.img, (self.hero.get_rect().center.x - self.cam.frame.width / 2 + self.cam.frame.left,
                                        self.hero.get_rect().center.y - self.cam.frame.height / 2 + self.cam.frame.top))

        self.window.blit(pygame.transform.scale(self.canvas, [self.screen_size.x * self.cam.coefficient,
                                                              self.screen_size.y * self.cam.coefficient]),
                         (-self.cam.frame.width, -self.cam.frame.height))

if __name__ == '__main__':
    game = Game(Vector2D(1280, 720), 'Multiverse')

    game.include_resources()
    game.new()
    game.run()