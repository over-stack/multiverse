from copy import deepcopy
import random
import numpy as np
from entity import Entity
from spawn import Spawn


class EvolutionExample:
    def __init__(self, entity, min_, max_, area):
        self.entity = entity
        self.min_ = min_
        self.max_ = max_
        self.area = area  # spawn-area


class Evolution:
    def __init__(self, spawn):
        self.spawn = spawn
        self.examples = dict()
        self.ids = dict()

    def add_example(self, name, example):
        self.examples[name] = example
        self.ids[name] = list()

    def delete_example(self, name):
        del self.examples[name]

    def generate(self, example_name, count, nextgen=False):
        example = self.examples[example_name]
        new_ids = self.spawn.spawn_random('entities', count, example.area, example.entity, return_id=True)
        self.ids[example_name].extend(new_ids)

        if nextgen:
            for id_ in new_ids:
                rand_id = random.choice(self.ids[example_name])
                rand_genome = self.spawn.containers['entities'][rand_id].genome
                self.spawn.containers['entities'][id_].set_genome(rand_genome, mutation=True)

    def delete_id(self, id_):
        for example_name in self.examples:
            if id_ in self.ids[example_name]:
                self.ids[example_name].remove(id_)

    def update(self, time):
        for example_name in self.ids:
            example = self.examples[example_name]
            survived = len(self.ids[example_name])
            print(f'survived: {survived}')
            if survived == 0:
                self.generate(example_name, example.max_ - survived)
            elif survived < example.min_:
                self.generate(example_name, example.max_ - survived, nextgen=True)
