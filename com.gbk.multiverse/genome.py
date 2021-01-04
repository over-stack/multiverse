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
            '''
            print('************')
            print(x)
            print('---------------')
            print(layer.shape)
            print(layer)
            print('************')
            '''
            x = self.relu(x.dot(layer))
        return x

    def sigmoid(self, x):
        result = 1 / (1 + np.exp(-x))
        return result

    def relu(self, x):
        x[x<0] = 0
        return x

    def save(self, filename):
        np.save(filename, self.network)

    def load(self, filename):
        weights = np.load(filename, allow_pickle=True)
        for i in range(len(self.network)):
            self.network[i] = weights[i][0]

    def copy(self):
        return deepcopy(self)
