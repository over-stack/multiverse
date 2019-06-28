from object import Object

class Decoration(Object):
    def __init__(self, animanager, position, max_health, id_, family='single', type='decoration'):
        Object.__init__(self, animanager, position, id_, max_health, family, type)

    def update(self, time):
        Object.update(self, time)