from copy import deepcopy

class Animation:
    def __init__(self, sheet, cols, rows, count, speed, looped=False):
        self.speed = speed

        self.sheet = sheet

        self.cols = cols
        self.rows = rows
        self.count = count

        self.rect = self.sheet.get_rect()
        self.width = self.rect.width / cols
        self.height = self.rect.height / rows
        self.depth = self.height / 2 # axis z

        self.frames = [(index % cols * self.width, index // cols * self.height, self.width, self.height)
                       for index in range(self.count)] # like rects

        self.center = (self.width // 2, self.height // 2)

        self.currentFrame = 0.0
        self.frames_count = len(self.frames)
        self.isPlaying = True
        self.looped = looped

    def tick(self, time):
        if not self.isPlaying:
            return False

        self.currentFrame += self.speed * time

        if self.currentFrame > self.count - 1:
            if not self.looped:
                self.isPlaying = False
                self.currentFrame = self.count - 1  # stopping on the last frame
            else:
                self.currentFrame -= self.count - 1

    def __deepcopy__(self, memo):  # makes copy without copying sheet
        return Animation(self.sheet, deepcopy(self.cols, memo), deepcopy(self.rows, memo),
                         deepcopy(self.count, memo), deepcopy(self.speed, memo), deepcopy(self.looped, memo))
