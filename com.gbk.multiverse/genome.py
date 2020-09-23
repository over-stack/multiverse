from copy import deepcopy
import numpy as np


class Genome:
    def __init__(self, layers):
        self.layers = layers
        self.network = [2 * np.random.rand(layers[i], layers[i+1]) - 1 for i in range(len(layers) - 1)]
        self.probCrossover = 1
        self.probMutation = 0.2
        self.ncount = sum([layer.size for layer in self.network])

    def evaluate(self, features):
        x = np.array(features)
        for layer in self.network:
            x = self.sigmoid(x.dot(layer))
        return x

    def sigmoid(self, x):
        result = 1 / (1 + np.exp(-x))
        return result

    def save(self, filename):
        np.save(filename, self.network)

    def load(self, filename):
        self.network = np.load(filename)

    def copy(self):
        return deepcopy(self)
