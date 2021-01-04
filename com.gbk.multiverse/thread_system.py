import threading

from my_libs import Rect, Vector2D

class VCIThread(threading.Thread):
    def __init__(self, entities, decorations, time_, range_, frame_mod, frame):
        threading.Thread.__init__(self)
        self.time_ = 0
        self.range_ = None
        self.entities = entities
        self.decorations = decorations
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
                rect = ent.get_rect()
                area = Rect(rect.center.x, rect.center.y,
                            ent.vision_area.x, ent.vision_area.y, isCenter=True)
                entities_around = [_ for _ in self.entities if _.alive and _.get_rect().intersects(area) and _ is not ent]
                decorations_around = [_ for _ in self.decorations if _.get_rect().intersects(area)]
                #objects_around = entities_around + decorations_around
                #world_around = self.game_world.get_world_around(ent.get_rect().center)
                #self.game_env.apply(entity=ent, objects_around=objects_around)

                ent.control(self.time_, entities_around, decorations_around, i % self.frame_mod != self.frame)


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