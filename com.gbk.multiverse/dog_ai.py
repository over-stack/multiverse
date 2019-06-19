import numpy as np
from entity import Entity

class dog_ai:

    def __init__(self):
        self.inputs = []
        self.outputs = list(np.random.rand(1, 5))

    def get_vision(self, health, satiety, position, strength, speed, entities):

        ent_health = [ent.health for ent in entities]
        ent_satiety = [ent.satiety for ent in entities]
        ent_position = [ent.position for ent in entities]
        ent_strength = [ent.strength for ent in entities]
        ent_speed = [ent.speed for ent in entities]

        self.inputs =[health, satiety, position, strength, speed, entities,
                      ent_health, ent_satiety, ent_position, ent_strength, ent_speed]

