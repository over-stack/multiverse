import pygame
from animationManager import AnimationManager
from entity import Entity

pygame.init()
window = pygame.display.set_mode((1920, 1080))

pygame.display.set_caption('Multiverse')

fps = 60

resources_dir = 'resources/gothicvania patreon collection/'

anim_hero = AnimationManager()

anim_hero.create(name='stay', filename=resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-idle.png',
            cols=4, rows=1, count=4, speed=0.5)
anim_hero.create(name='attack', filename=resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-attack.png',
            cols=6, rows=1, count=6, speed=0.5)
anim_hero.create(name='walk', filename=resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-run.png',
            cols=12, rows=1, count=12, speed=0.5)

hero = Entity(animanager=anim_hero, position=[50, 50], speed=5, health=100, strength=10)

anim_dog = AnimationManager()

anim_dog.create(name='stay', filename=resources_dir + 'Hell-Hound-Files/PNG/hell-hound-idle.png',
            cols=6, rows=1, count=6, speed=0.5)
anim_dog.create(name='walk', filename=resources_dir + 'Hell-Hound-Files/PNG/hell-hound-walk.png',
            cols=12, rows=1, count=12, speed=0.5)

dog = Entity(animanager=anim_dog, position=[200, 200], speed=7, health=80, strength=14)

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

    ####### CONTROLS #######
    hero.control(keys)

    ####### COLLISION ######
    hero.check_collision([dog])

    ####### UPDATES ########
    hero.update(time)
    dog.update(time)

    pygame.display.update()

    window.fill((0, 0, 0)) # Makes black window

    ####### DRAW #########
    hero.draw(window)
    dog.draw(window)

pygame.quit()