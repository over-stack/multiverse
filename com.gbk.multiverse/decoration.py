from object import Object

class Decoration(Object):

    def __init__(self, animanager, position, max_health, id):
        Object.__init__(self, animanager, position, id, max_health)

    def update(self, time):
        Object.update(self, time)