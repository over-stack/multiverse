import random
import numpy as np


class EvolutionAlg:
    def __init__(self, input_size, output_size):
        self.feature_dim = 5
        self.features_count = 10
        self.preprocessed_dim = 1
        self.genome_out_params = 6
        self.output_dim = 6

        self.genomes = dict()

    def generate_population(self, ids):
        for id_ in ids:
            self.genomes[id_] = self.generate_genome()

    def generate_genome(self):
        return 2 * np.random.rand(self.input_size, self.output_size) - 1

    def generate_gen(self):
        return 2 * np.random.rand(1)[0] - 1

    def crossover(self, pair, free_id):
        choice = self.make_choice()
        self.genomes[free_id] = self.genomes[pair[0]].copy()
        self.genomes[free_id][:choice[0], :choice[1]] = self.genomes[pair[1]][:choice[0], :choice[1]].copy()

    def mutation(self, id_):
        choice = self.make_choice()
        self.genomes[id_][choice[0], choice[1]] = self.generate_gen()

    def inversion(self, id_):
        choice = self.make_choice()
        pass

    def make_decision(self, features, id_):
        features = np.array(features)
        result = self.sigmoid(features.dot(self.genomes[id_]))
        return np.argmax(result)

    def save_genome(self, filename, id_):  # Check
        with open(filename, 'w') as f:
            f.writelines(self.genomes[id_])

    def load_genome(self, filename, id_):  # Add formatting
        with open(filename, 'r') as f:
            self.genomes[id_] = f.readlines()

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def distance(self, position1, position2):
        return ((position2[0] - position1[0]) ** 2 + (position2[1] - position1[1]) ** 2) ** 0.5

    def make_choice(self):
        choice = [int(random.uniform(0, 1) * self.input_size),
                  int(random.uniform(0, 1) * self.output_size)]
        return choice
