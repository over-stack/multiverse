from pygame import image

class World:

    def __init__(self, filename, size, tile_size):
        self.image = image.load(filename)
        self.size = size
        self.tile_size = tile_size
        self.matrix = [[0 for i in range(size[0])] for j in range(size[1])]
        self.tiles = dict()

    def add_tile(self, position, code):
        self.tiles[code] = position

    def generate_matrix(self, size):
        pass

    def draw(self, surface, scroll, position, radius):

        left = int(position[0] // self.tile_size[0] - radius)
        right = int(position[0] // self.tile_size[0] + radius)
        top = int(position[1] // self.tile_size[1] - radius)
        bottom = int(position[1] // self.tile_size[1] + radius)

        if left < 0:
            left = 0

        if right < 0:
            right = 0

        if top < 0:
            top = 0

        if bottom < 0:
            bottom = 0

        if left > self.size[0]:
            left = self.size[0]

        if right > self.size[0]:
            right = self.size[0]

        if top > self.size[1]:
            top = self.size[1]

        if bottom > self.size[1]:
            bottom = self.size[1]

        for y in range(top, bottom):
            for x in range(left, right):
                tile = self.tiles[self.matrix[y][x]]
                surface.blit(self.image, (x * self.tile_size[0] + scroll[0],
                                          y * self.tile_size[1] + scroll[1]), tile + self.tile_size)