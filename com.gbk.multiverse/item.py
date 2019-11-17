from object import Object


class Item(Object):
    def __init__(self, animanager, position, bonuses, weight, id_, family='single', type_='item'):
        Object.__init__(animanager, position, id_, family=family, type_=type_)

        self.isCollision = False
        self.dropped = True
        self.bonuses = bonuses
        self.weight = weight

        '''
        self.health_bonus = 10
        self.regeneration_bonus = 0.1
        self.satiety_bonus = 0
        self.satiety_speed_bonus = 0
        self.speed_bonus = 0
        self.strength_bonus = 0
        '''
