import threading

from my_libs import Rect, Vector2D

class VCIThread(threading.Thread):
    def __init__(self, collision_table, entities, time_, range_, frame_mod, frame):
        threading.Thread.__init__(self)
        self.time_ = 0
        self.range_ = None
        self.collision_table = collision_table
        self.entities = entities
        self.frame_mod = 1
        self.frame = 0
        self.time_ = time_
        self.range_ = range_
        self.frame_mod = frame_mod
        self.frame = frame

    def run(self):
        for i in self.range_:
            # Vision
            ent = self.entities[i]
            if ent.ai:
                entities_around = self.collision_table[ent]
                ent.control(self.time_, entities_around, [], i % self.frame_mod != self.frame)


class myThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        print(self.name)

if __name__ == '__main__':
    thread1 = myThread('abc')
    thread2 = myThread('def')

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()