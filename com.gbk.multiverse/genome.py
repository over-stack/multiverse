from functools import reduce
from copy import deepcopy
import random
import numpy as np


class Genome:
    def __init__(self, layers):
        self.layers = layers
        self.memory = list()
        for i in range(len(layers) - 1):
            self.memory.append(2 * np.random.rand(layers[i], layers[i + 1]) - 1)
        self.memory = np.array(self.memory)

    def mutation(self):
        nmem = int(random.uniform(0, 1) * self.memory.shape[0])
        choice = [int(random.uniform(0, 1) * self.memory[nmem].shape[0]),
                  int(random.uniform(0, 1) * self.memory[nmem].shape[1])]
        self.memory[nmem][choice[0], choice[1]] = random.uniform(0, 1) * 10  # 10 = range

    def evaluate(self, features):
        features = list(reduce(lambda x, y: x + y, features))
        features = np.array(features)
        result = self.sigmoid(features.dot(self.memory[0]))
        for i in range(1, self.memory.shape[0]):
            result = self.sigmoid(result.dot(self.memory[i]))
        encoded_results = list()
        for i in range(result.shape[0]):
            if result[i] > 0.5:
                encoded_results.append(i)
        return encoded_results

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def save_genome(self, filename, id_):
        pass

    def load_genome(self, filename, id_):
        pass

    def copy(self):
        return deepcopy(self)
