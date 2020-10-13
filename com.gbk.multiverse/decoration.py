from object import Object


class Decoration(Object):
    def __init__(self, animanager, max_health, family='single', container='decorations'):
        Object.__init__(self, animanager, max_health, family, container)
