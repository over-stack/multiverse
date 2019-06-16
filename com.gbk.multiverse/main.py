import pygame
from animationManager import AnimationManager
from entity import Entity

pygame.init()
window = pygame.display.set_mode((1920, 1080))

pygame.display.set_caption('Multiverse')

fps = 60

resources_dir = 'resources/gothicvania patreon collection/'

anim = AnimationManager()

anim.create(name='idle', filename=resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-idle.png',
            cols=4, rows=1, count=4, speed=0.5)
anim.create(name='attack', filename=resources_dir + 'Gothic-hero-Files/PNG/gothic-hero-attack.png',
            cols=6, rows=1, count=6, speed=0.5)

ent = Entity(animanager=anim, x=50, y=50, speed=5, health=100, strength=10)

Clock = pygame.time.Clock()

run = True
while run:
    Clock.tick(fps)

    time = Clock.get_time()
    time = time / 80 # game speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    ent.animanager.set('idle') # default animation for ent

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        ent.move_x(-time)

        ent.animanager.flip(True)

    if keys[pygame.K_d]:
        ent.move_x(time)

        ent.animanager.flip(False)

    if keys[pygame.K_w]:
        ent.move_y(-time)

    if keys[pygame.K_s]:
        ent.move_y(+time)

    if keys[pygame.K_SPACE]:
        anim.set('attack')

    ent.update(time)

    pygame.display.update()

    window.fill((0, 0, 0))
    ent.draw(window)

pygame.quit()