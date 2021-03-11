from object import Object
from entity import Entity


class Item(Object):
    def __init__(self, animanager, weight=0, family='single', container='items'):
        Object.__init__(self, animanager, max_health=100, family=family, container=container)

        self.isCollision = False
        self.draw_bars = False
        self.dropped = True
        self.weight = weight

        '''
        self.health_bonus = 10
        self.regeneration_bonus = 0.1
        self.satiety_bonus = 0
        self.satiety_speed_bonus = 0
        self.speed_bonus = 0
        self.strength_bonus = 0
        '''
    def pick(self, entity):
        pass


class Food(Item):
    def __init__(self, animanager, satiety_bonus):
        Item.__init__(self, animanager)

        self.satiety_bonus = satiety_bonus

    def pick(self, entity):
        if self.dropped:
            entity.satiety += self.satiety_bonus
            if entity.satiety >= entity.max_satiety:
                entity.satiety = entity.max_satiety
            self.dropped = False
