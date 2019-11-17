from copy import deepcopy
import random
import numpy as np
from entity import Entity
from spawn import Spawn
from genome import Genome

COUNT_OF_BUTTONS = 323


class EvolutionExample:
    def __init__(self, entity, min_, max_, area):
        self.entity = entity
        self.min_ = min_
        self.max_ = max_
        self.area = area  # spawn-area


class Evolution:
    def __init__(self, spawn, codes):
        self.spawn = spawn
        self.codes = codes
        self.encoder = dict()
        for i in range(len(self.codes)):
            self.encoder[codes[i]] = i / len(self.codes)
        self.examples = dict()
        self.genomes = dict()
        self.layers = [880, 5]
        self.buttons = {0: ' ', 1: 'a', 2: 'w', 3: 'd', 4: 's'}

    def add_example(self, name, example):
        self.examples[name] = example
        self.genomes[name] = dict()

    def delete_example(self, name):
        del self.examples[name]

    def generate(self, example_name, count, nextgen=False):
        example = self.examples[example_name]
        ids = self.spawn.spawn_random('entities', count, example.area, example.entity, return_id=True)
        for id_ in ids:
            if not nextgen:
                self.genomes[example_name][id_] = Genome(self.layers)
            else:
                new_genome = random.choice(list(self.genomes[example_name].values())).copy()
                new_genome.mutation()
                self.genomes[example_name][id_] = new_genome

    def delete_entity(self, id_):
        for example_name in self.genomes:
            if id_ in self.genomes[example_name]:
                del self.genomes[example_name][id_]
                return

    def update(self, time):
        for example_name in self.genomes:
            example = self.examples[example_name]
            survived = len(self.genomes[example_name])
            print(f'survived: {survived}')
            if survived == 0:
                self.generate(example_name, example.max_ - survived)
            elif survived < example.min_:
                self.generate(example_name, example.max_ - survived, nextgen=True)

    def action(self, id_, features):
        for example_name in self.genomes:
            if id_ in self.genomes[example_name]:
                keys = [0 for i in range(COUNT_OF_BUTTONS)]
                result = self.genomes[example_name][id_].evaluate(self.encode_features(features))
                for r in result:
                    keys[ord(self.buttons[r])] = 1
                return keys

    def encode_features(self, features):
        features = [[self.encoder[j] for j in features[i]] for i in range(len(features))]
        # print(self.codes)
        # for i in range(len(features)):
        # for j in range(len(features[i])):
        # print(features[i][j], ': ', end=' ')
        # print(self.encoder[features[i][j]])
        return features
