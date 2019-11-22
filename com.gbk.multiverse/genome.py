from copy import deepcopy
import random
import numpy as np
from scipy import signal
import skimage.measure


class Genome:
    def __init__(self):
        self.network = {'conv2d_1': 2 * np.random.rand(3, 3) - 1,
                        'maxpool2d_1': (2, 2),
                        'conv2d_2': 2 * np.random.rand(3, 3) - 1,
                        'maxpool2d_2': (2, 2),
                        'dense_1': 2 * np.random.rand(36, 10) - 1,
                        'dense_2': 2 * np.random.rand(10, 5) - 1}
        self.memlayers = ['conv2d_1', 'conv2d_2', 'dense_1', 'dense_2']

        # print('conv2d: ', self.network['conv2d_1'])

    def mutation(self, count=3):
        layer_name = random.choice(self.memlayers)
        layer = self.network[layer_name]
        choice = [int(random.uniform(0, 1) * layer.shape[0]),
                  int(random.uniform(0, 1) * layer.shape[1])]
        # print()
        # print(self.network[layer_name])
        layer[choice[0], choice[1]] = random.uniform(0, 1) * 20 - 10
        # print(self.network[layer_name])
        # print()
        count -= 1
        if count > 0:
            self.mutation(count)

    def evaluate(self, features):
        features = np.stack(features)
        result = signal.convolve2d(features, np.rot90(self.network['conv2d_1'], 2), 'valid')
        result = skimage.measure.block_reduce(result, self.network['maxpool2d_1'], np.max)
        result = signal.convolve2d(result, np.rot90(self.network['conv2d_2'], 2), 'valid')
        result = skimage.measure.block_reduce(result, self.network['maxpool2d_2'], np.max)
        result = result.flatten()
        result = self.sigmoid(result.dot(self.network['dense_1']))
        result = self.sigmoid(result.dot(self.network['dense_2']))
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
