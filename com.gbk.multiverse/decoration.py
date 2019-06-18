from object import Object

class Decoration(Object):

    def __init__(self, animanager, position, health):
        Object.__init__(self, animanager, position)

        self.health = health

    def update(self, time):
        Object.update(self, time)