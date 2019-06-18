import pygame
from animationManager import AnimationManager
from entity import Entity
from world import World
from camera import Camera
from decoration import Decoration

pygame.init()
screen_size = (800, 400)
window = pygame.display.set_mode(screen_size)

pygame.display.set_caption('Multiverse')

fps = 60

cam = Camera(screen_size=screen_size)

resources_dir = 'resources/gothicvania patreon collection/'
resources_dir1 = 'resources/tiny-RPG-forest-files/PNG/environment/'

game_world = World(filename=resources_dir1 + 'tileset.png', size=(100, 100), tile_size=(16, 16))
game_world.add_tile(position=(208, 288), code=0)

anim_dec = AnimationManager()

anim_dec.create(name='stay', filename=resources_dir1 + '/sliced-objects/tree-pink.png',
                            cols = 1, rows=1, count=1, speed=0)

tree = Decoration(animanager=anim_dec, position=[200, 200], health=100)

anim_hero = AnimationManager()

anim_hero.create(name='stay', filename=resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-idle.png',
            cols=4, rows=1, count=4, speed=0.5, looped=True)
anim_hero.create(name='attack', filename=resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-attack.png',
            cols=6, rows=1, count=6, speed=0.5)
anim_hero.create(name='walk', filename=resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-run.png',
            cols=12, rows=1, count=12, speed=0.5, looped=True)

hero = Entity(animanager=anim_hero, position=[0, 0], speed=5, health=100, strength=10)

anim_dog = AnimationManager()

anim_dog.create(name='stay', filename=resources_dir + 'Hell-Hound-Files/PNG/hell-hound-idle.png',
            cols=6, rows=1, count=6, speed=0.5, looped=True)
anim_dog.create(name='walk', filename=resources_dir + 'Hell-Hound-Files/PNG/hell-hound-walk.png',
            cols=12, rows=1, count=12, speed=0.5, looped=True)

dog = Entity(animanager=anim_dog, position=[800, 250], speed=7, health=80, strength=14)

decorations = [tree]
entities = [hero, dog]

Clock = pygame.time.Clock()

run = True
while run:
    Clock.tick(fps)

    time = Clock.get_time()
    time = time / 80 # game speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    dog.acceleration[0] = -5

    hero.control(keys)

    for ent in entities:
        ent.check_collision(entities + decorations)

    for dec in decorations:
        dec.update(time)

    for ent in entities:
        ent.update(time)

    cam.update(hero.position)
    pygame.display.update()

    window.fill((0, 0, 0)) # Makes black window

    objects = decorations + entities

    objects.sort(key=lambda obj: obj.position[1]) # sorting objects by y axis

    game_world.draw(window, cam.frame, hero.position, radius=10) # draw map

    for obj in objects: # draw objects
        obj.draw(window, cam.frame)

pygame.quit()