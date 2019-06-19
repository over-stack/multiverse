from pygame import image

class World:

    def __init__(self, filename, size, tile_size):
        self.image = image.load(filename)
        self.size = size
        self.size_in_tiles = [size[0] // tile_size[0], size[1] // tile_size[1]]
        self.tile_size = tile_size
        self.matrix = [[0 for i in range(self.size_in_tiles[0])] for j in range(self.size_in_tiles[1])]
        self.tiles = dict()

    def add_tile(self, position, code):
        self.tiles[code] = position

    def generate_matrix(self, size):
        pass

    def draw(self, surface, scroll, position, radius):

        left = int((position[0] - radius) // self.tile_size[0])
        right = int((position[0] + radius) // self.tile_size[0])
        top = int((position[1] - radius) // self.tile_size[1])
        bottom = int((position[1] + radius) // self.tile_size[1])

        if left < 0:
            left = 0

        if right < 0:
            right = 0

        if top < 0:
            top = 0

        if bottom < 0:
            bottom = 0

        if left > self.size_in_tiles[0]:
            left = self.size_in_tiles[0]

        if right > self.size_in_tiles[0]:
            right = self.size_in_tiles[0]

        if top > self.size_in_tiles[1]:
            top = self.size_in_tiles[1]

        if bottom > self.size_in_tiles[1]:
            bottom = self.size_in_tiles[1]

        for y in range(top, bottom):
            for x in range(left, right):
                tile = self.tiles[self.matrix[y][x]]
                surface.blit(self.image, (x * self.tile_size[0] + scroll[0],
                                          y * self.tile_size[1] + scroll[1]), tile + self.tile_size)