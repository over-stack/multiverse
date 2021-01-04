import pygame
from copy import copy, deepcopy

from my_libs import Rect, Vector2D

class ScrollBar:
    def __init__(self):
        pass

class ParamBar:
    def __init__(self):
        pass

class List:
    def __init__(self):
        pass

class Text:
    def __int__(self, text, font, color=(0, 0, 0)):
        self.font = font
        self.text = text
        self.text_rendered = font.render(text, False, (0, 0, 0))

class Layer:
    def __init__(self, position, size, color):
        self.position = position
        self.size = size
        self.color = color
        self.bars = list()

    def add_bar(self, bar):
        #new_bar = copy(bar)
        new_bar = bar
        new_bar.move(self.position)
        self.bars.append(new_bar)

    def update(self):
        for bar in self.bars:
            bar.update()

    def handle_mouse(self, event):
        for bar in self.bars:
            bar.handle_mouse(event)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position.x, self.position.y, self.size.x, self.size.y))
        for bar in self.bars:
            bar.draw(surface)

    def move(self, delta):
        self.position.x += delta.x
        self.position.y += delta.y
        for bar in self.bars:
            bar.move(delta)

class Window(Layer):
    def __init__(self, position, size, color):
        Layer.__init__(self, position, size, color)
        close_button = Button(position=Vector2D(self.position.x + self.size.x - 50, self.position.y),
                              size=Vector2D(50, 25), color=(255, 0, 0), action=self.close)
        self.bars.append(close_button)
        self.closed = False
        self.active = True
        self.subwindow = None
        self.shadow = pygame.Surface((self.size.x, self.size.y))
        self.shadow.set_alpha(100)
        self.shadow.fill((0, 0, 0))

    def close(self):
        if not self.closed:
            self.closed = True
            self.active = False

    def open(self):
        if self.closed:
            self.closed = False
            self.active = True
        return self

    def update(self):
        if not self.closed:
            if self.active:
                Layer.update(self)
            else:
                self.subwindow.update()

    def handle_mouse(self, event):
        if not self.closed:
            if self.active:
                for bar in self.bars:
                    result = bar.handle_mouse(event)
                    if result and result.__class__.__name__ == 'Window':
                        self.subwindow = result
                        self.active = False
            else:
                self.subwindow.handle_mouse(event)
                if self.subwindow.closed:
                    self.active = True
                    self.subwindow = None

    def draw(self, surface):
        if not self.closed:
            if self.active:
                Layer.draw(self, surface)
            else:
                pygame.draw.rect(surface, self.color, (self.position.x, self.position.y, self.size.x, self.size.y))
                for bar in self.bars:
                    if not bar is self.subwindow:
                        if not bar is self.subwindow:
                            bar.draw(surface)

                surface.blit(self.shadow, (self.position.x, self.position.y))
                self.subwindow.draw(surface)

class Button:
    def __init__(self, position, size, color, action, font=None, text_before='', text_after=''):
        self.position = position
        self.size = size
        self.color = color
        self.action = action
        self.highlighted = False
        self.pressed = False
        self.switched = False
        self.active = True

        self.text_before_rendered = None
        self.text_after_rendered = None
        if text_before:
            self.text_before_rendered = font.render(text_before, False, (0, 0, 0))
            text_before_rect = self.text_before_rendered.get_rect()
            self.text_before_position = [self.position.x + (self.size.x - text_before_rect.width) // 2,
                                         self.position.y + (self.size.y - text_before_rect.height) // 2]
        if text_after:
            self.text_after_rendered = font.render(text_after, False, (0, 0, 0))
            text_after_rect = self.text_after_rendered.get_rect()
            self.text_after_position = [self.position.x + (self.size.x - text_after_rect.width) // 2,
                                        self.position.y + (self.size.y - text_after_rect.height) // 2]

    def on_click(self):
        return self.action()

    def set_active(self, value):
        self.active = value

    def update(self):
        pos = pygame.mouse.get_pos()
        if self.position.x <= pos[0] <= self.position.x + self.size.x and \
                                self.position.y <= pos[1] <= self.position.y + self.size.y:
            self.highlighted = True
        else:
            self.highlighted = False

    def handle_mouse(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.highlighted and self.active and not self.pressed:
            self.switched = not self.switched
            self.pressed = True
        if event.type == pygame.MOUSEBUTTONUP and self.pressed:
            self.pressed = False
            if self.highlighted:
                return self.on_click()

    def draw(self, surface):
        if not self.highlighted and self.active:
            color = self.color
        else:
            if self.pressed:
                color = list(i // 3 for i in self.color)
            else:
                color = list(i // 1.5 for i in self.color)

        pygame.draw.rect(surface, color, (self.position.x, self.position.y, self.size.x, self.size.y))
        if self.text_before_rendered and not self.switched:
            surface.blit(self.text_before_rendered, self.text_before_position)
        if self.text_after_rendered and self.switched:
            surface.blit(self.text_after_rendered, self.text_after_position)

    def move(self, delta):
        if self.text_before_rendered:
            self.text_before_position[0] += delta.x
            self.text_before_position[1] += delta.y
        if self.text_after_rendered:
            self.text_after_position[0] += delta.x
            self.text_after_position[1] += delta.y
        self.position.x += delta.x
        self.position.y += delta.y


class Bar:
    def __init__(self, length, height, width, colors):
        self.length = length
        self.height = height
        self.width = width
        self.colors = dict([(key, colors[key]) for key in sorted(colors.keys(), reverse=True)])

    def draw(self, surface, param, max_param, param_bonus, center, cam_scroll):
        scaled = param / ((max_param + param_bonus) / self.length)

        color = (0, 255, 0)
        for key in sorted(self.colors.keys(), reverse=True):
            if scaled <= key * (self.length / 100):
                color = self.colors[key]

        position = Vector2D(center.x + cam_scroll.x, center.y + cam_scroll.y)
        pygame.draw.rect(surface, color,
                         (position.x - scaled / 2, position.y - self.height / 2, scaled, self.width))