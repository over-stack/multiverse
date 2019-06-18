from object import Object

class Item(Object):

    def __init__(self, animanager, position):
        Object.__init__(animanager, position)

        self.collision = False
        self.dropped = True