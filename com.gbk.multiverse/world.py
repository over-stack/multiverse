from pygame import image

class World:

    def __init__(self, filename, size):
        self.image = image.load(filename)
        self.size = size
        self.matrix = [[0 for i in range(size[0])] for j in range(size[1])]
        self.tiles = dict()

    def add_tile(self, position, size, code):
        self.tiles[code] = position + size

    def generate_matrix(self, size):
        pass

    def draw(self, surface, scroll):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.matrix[y][x] == 0:
                    tile = self.tiles[self.matrix[y][x]]
                    surface.blit(self.image, (x * tile[2] + scroll[0], y * tile[3] + scroll[1]), tile)