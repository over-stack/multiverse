import numpy as np
import time
from genome import Genome
from my_libs import Rect, Vector2D


class EvolutionExample:
    def __init__(self, entity, min_, max_, area):
        self.entity = entity
        self.min_ = min_
        self.max_ = max_
        self.area = area  # spawn-area
        self.shift = Vector2D(0, 0)
        self.spawning = True
        self.start = time.monotonic()
        self.duration = 10
        self.epoch = 0
        self.current_population = 0
        self.mutation_prob = 0.2


class Evolution:
    def __init__(self, spawn):
        self.spawn = spawn
        self.examples = dict()
        self.entities = dict()

    def add_example(self, example, start_genome_file=''):
        self.examples[example.entity.family] = example
        self.entities[example.entity.family] = list()

        genomes = list()
        if start_genome_file:
            start_genome = Genome(example.entity.genome_layers)
            start_genome.load(start_genome_file)
            for i in range(example.max_):
                genomes.append(start_genome)
        self.generate(example.entity.family, genomes)

    def delete_example(self, name):
        del self.examples[name]
        self.remove_entities(name)

    def generate(self, example_name, genomes=None):
        example = self.examples[example_name]
        entities = self.spawn.spawn_random(example.max_, example.area, example.entity, example.shift,
                                           return_obj=True)
        self.entities[example_name] = entities
        example.current_population = example.max_
        example.epoch += 1
        example.start = time.monotonic()

        if genomes:
            for i in range(len(entities)):
                entities[i].set_genome(genomes[i])

    def remove_entities(self, example_name):
        self.spawn.remove_family('entities', example_name)
        del self.entities[example_name]
        self.entities[example_name] = list()

    def update(self):
        for example_name in self.examples:
            example = self.examples[example_name]
            if example.current_population < example.min_ or time.monotonic() - example.start > example.duration:
                entities = self.entities[example_name]
                entities.sort(key=lambda x: x.score, reverse=True)
                probabilities = list()
                score_sum_ = 0
                #print(example_name)
                #print('Epoch:', example.epoch)
                for ent in entities:
                    probabilities.append(ent.score)
                    score_sum_ += ent.score
                    #print(ent.score, end=' ')
                #print('\n////////////', score_sum_, '/////////////////')

                probabilities = [p / score_sum_ for p in probabilities]
                pool = np.random.choice(entities, example.max_, p=probabilities)
                np.random.shuffle(pool)
                genomes = list()
                for i in range(0, len(pool), 2):
                    d = np.random.randint(pool[i].genome.ncount)
                    genomes.append(self.crossover(pool[i], pool[i+1], d, example.mutation_prob))
                    genomes.append(self.crossover(pool[i+1], pool[i], d, example.mutation_prob))

                self.remove_entities(example_name)
                self.generate(example_name, genomes)

    def crossover(self, ent1, ent2, d, mutation_prob):
        genome = Genome(ent1.genome_layers)
        count = 0
        for nlayer in range(len(genome.network)):
            for i in range(len(genome.network[nlayer])):
                for j in range(len(genome.network[nlayer][i])):
                    if count <= d:
                        genome.network[nlayer][i, j] = ent1.genome.network[nlayer][i, j]
                    else:
                        genome.network[nlayer][i, j] = ent2.genome.network[nlayer][i, j]
                    if np.random.uniform(0, 1) < mutation_prob:
                        genome.network[nlayer][i, j] += np.random.uniform(-1, 1) * 100
                    count += 1
        return genome

    def archive(self, family):
        if family in self.examples.keys():
                self.examples[family].current_population -= 1
