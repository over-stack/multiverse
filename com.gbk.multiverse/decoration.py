from object import Object

class Decoration(Object):
    def __init__(self, animanager, position, max_health, family='single', type_='decoration'):
        Object.__init__(self, animanager, position, max_health, family, type_)