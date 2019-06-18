from pygame import image

class Animation:

    def __init__(self, filename, cols, rows, count, speed, looped=False):
        self.speed = speed

        self.sheet = image.load(filename)

        self.cols = cols
        self.rows = rows
        self.count = count

        self.rect = self.sheet.get_rect()
        self.width = self.rect.width / cols
        self.height = self.rect.height / rows

        self.frames = [(index % cols * self.width, index // cols * self.height, self.width, self.height)
                       for index in range(self.count)]

        self.center = (self.width // 2, self.height // 2)

        self.currentFrame = 0.0
        self.isPlaying = True
        self.looped = looped

    def tick(self, time):
        if not self.isPlaying:
            return False

        self.currentFrame += self.speed * time

        if self.currentFrame > self.count:
            self.currentFrame -= self.count
            self.isPlaying = False