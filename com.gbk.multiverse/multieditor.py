import pygame
from camera import Camera
from my_libs import Vector2D
from GUI import Button, Layer, Window
from game import *

def foo():
    print('*********')

class MultiEditor:
    def __init__(self, screen_size, title):
        self.screen_size = screen_size
        self.title = title
        self.fps = 60

        pygame.init()
        self.window = pygame.display.set_mode(screen_size.get_tuple(),
                                              pygame.HWSURFACE | pygame.DOUBLEBUF)  # only for draw the canvas
        self.canvas = self.window.copy()  # used to draw

        pygame.display.set_caption(title)

        self.cam = Camera(screen_size=self.screen_size, coefficient=1)

        font = pygame.font.SysFont('serif', 20)
        font.set_bold(True)

        self.button_create = Button(position=Vector2D(0, 0), size=Vector2D(100, 50), color=(213, 135, 56), action=game.run,
                             font=font, text_before='CREATE', text_after='CREATE')
        self.button_load = Button(position=Vector2D(100, 0), size=Vector2D(100, 50), color=(213, 135, 56), action=foo,
                                 font=font, text_before='LOAD', text_after='LOAD')
        self.button_save = Button(position=Vector2D(200, 0), size=Vector2D(100, 50), color=(213, 135, 56), action=foo,
                                 font=font, text_before='SAVE', text_after='SAVE')
        self.button_about = Button(position=Vector2D(300, 0), size=Vector2D(100, 50), color=(213, 135, 56), action=foo,
                                  font=font, text_before='ABOUT', text_after='ABOUT')

        self.win1 = Window(position=Vector2D(420, 60), size=Vector2D(650, 650), color=(213, 180, 100))
        self.win2 = Window(position=Vector2D(100, 100), size=Vector2D(450, 450), color=(170, 143, 200))
        self.win2.close()

        self.button_create1 = Button(position=Vector2D(0, 0), size=Vector2D(100, 50), color=(213, 135, 56),
                                     action=self.win1.open,
                                     font=font, text_before='OPEN', text_after='OPEN')

        self.button_create2 = Button(position=Vector2D(0, 0), size=Vector2D(100, 50), color=(213, 135, 56),
                                     action=self.win2.open,
                                     font=font, text_before='OPEN', text_after='OPEN')
        self.win1.add_bar(self.button_create2)
        self.win1.add_bar(self.win2)
        self.win1.close()

        self.layer = Layer(position=Vector2D(10, 60), size=Vector2D(400, 650), color=(213, 200, 56))
        self.layer.add_bar(self.button_create1)

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

                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    self.button_create.handle_mouse(event)
                    self.button_load.handle_mouse(event)
                    self.button_save.handle_mouse(event)
                    self.button_about.handle_mouse(event)

                    self.layer.handle_mouse(event)

                    self.win1.handle_mouse(event)

            self.update(time)
            self.draw()

        pygame.quit()

    def update(self, time):
        self.button_create.update()
        self.button_load.update()
        self.button_save.update()
        self.button_about.update()

        self.layer.update()

        self.win1.update()

        self.cam.update(Vector2D(0,0))
        pygame.display.update()

    def draw(self):
        self.canvas.fill((220, 193, 250))  # Makes black window
        self.window.fill((220, 193, 250))
        self.window.blit(pygame.transform.scale(self.canvas, [self.screen_size.x * self.cam.coefficient,
                                                              self.screen_size.y * self.cam.coefficient]),
                         (-self.cam.frame.width, -self.cam.frame.height))

        self.button_create.draw(self.window)
        self.button_load.draw(self.window)
        self.button_save.draw(self.window)
        self.button_about.draw(self.window)

        self.layer.draw(self.window)

        self.win1.draw(self.window)


game = Game(Vector2D(1280, 720), 'Multiverse')
if __name__ == '__main__':
    multieditor = MultiEditor(Vector2D(1280, 720), 'Multieditor')
    multieditor.run()
