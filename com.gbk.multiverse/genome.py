from functools import reduce
from copy import deepcopy
import random
import numpy as np
from scipy import signal
import skimage.measure


class Genome:
    def __init__(self):
        self.conv2d_1 = np.array([[1, 0, 1],
                                  [0, 1, 0],
                                  [1, 0, 1]], dtype='float')
        self.conv2d_2 = np.array([[1, 0, 1],
                                  [0, 1, 0],
                                  [1, 0, 1]], dtype='float')
        self.layers = [36, 5]  # 32?
        self.memory = list()
        for i in range(len(self.layers) - 1):
            self.memory.append(2 * np.random.rand(self.layers[i], self.layers[i + 1]) - 1)
        self.memory = np.array(self.memory)

    def mutation(self):
        nmem = int(random.uniform(0, 1) * self.memory.shape[0])
        choice = [int(random.uniform(0, 1) * self.memory[nmem].shape[0]),
                  int(random.uniform(0, 1) * self.memory[nmem].shape[1])]
        self.memory[nmem][choice[0], choice[1]] = random.uniform(0, 1) * 10  # 10 = range

    def evaluate(self, features):
        features = np.stack(features)
        print(features.shape)
        result = signal.convolve2d(features, np.rot90(self.conv2d_1, 2), 'valid')
        print(result.shape)
        result = skimage.measure.block_reduce(result, (2, 2), np.max)
        print(result.shape)
        result = signal.convolve2d(result, np.rot90(self.conv2d_2, 2), 'valid')
        print(result.shape)
        result = skimage.measure.block_reduce(result, (2, 2), np.max)
        print(result.shape)
        result = result.flatten()
        print(result.shape)
        print()
        result = self.sigmoid(result.dot(self.memory[0]))
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
