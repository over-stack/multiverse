import numpy as np
import warnings
import re

file_tests = open('train/features.txt', 'r')
file_answers = open('train/answers.txt', 'r')


def scale(x, minx, maxx):
    if x > maxx:
        x = maxx

    if x < minx:
        x = minx

    l = maxx - minx
    return (x - minx) / l


def sigmoid(x, deriv=False):
    if deriv:
        return sigmoid(x) * (1 - sigmoid(x))
    else:
        return 1 / (1 + np.exp(-x))


def main():
    inputLayerSize = 9  # int(input("InputLayerSize: "))
    countOfHiddenLayers = 3  # int(input("CountOfHiddenLayers: "))
    hiddenLayerSize = [100, 100, 50, 50]  # [int(j) for j in input("HiddenLayerSize: ").split()]
    outputLayerSize = 5  # int(input("OutputLayerSize: "))

    # tests_count = int(input("Tests_count: "))

    # tests = [[float(j) for j in input("Test: ").split()] for i in range(tests_count)]
    lines_tests = file_tests.read()
    tests = [[float(j) for j in re.split('\s+', line)] for line in lines_tests.split('\n')]
    file_tests.close()

    X = np.array(tests)

    # answers = [[float(j) for j in input("Answers: ").split()] for i in range(outputLayerSize)]
    lines_answers = file_answers.read()
    answers = [[float(j) for j in re.split('\s+', line)] for line in lines_answers.split('\n')]
    file_answers.close()

    Y = np.array(answers)

    w = [float(i) for i in range(countOfHiddenLayers + 1)]

    w[0] = 2 * np.random.random((inputLayerSize, hiddenLayerSize[0])) - 1

    for i in range(1, countOfHiddenLayers):
        w[i] = 2 * np.random.random((hiddenLayerSize[i - 1], hiddenLayerSize[i])) - 1

    w[countOfHiddenLayers] = 2 * np.random.random((hiddenLayerSize[countOfHiddenLayers - 1], outputLayerSize)) - 1

    layers = [float(i) for i in range(countOfHiddenLayers + 2)]

    error = [float(j) for j in range(countOfHiddenLayers + 2)]
    delta = [float(j) for j in range(countOfHiddenLayers + 2)]

    countOfIterations = int(input("CountOfIterations: "))

    for i in range(countOfIterations):

        layers[0] = X

        for j in range(1, countOfHiddenLayers + 2):
            layers[j] = sigmoid(np.dot(layers[j - 1], w[j - 1]))

        error[countOfHiddenLayers + 1] = Y - layers[countOfHiddenLayers + 1]

        delta[countOfHiddenLayers + 1] = error[countOfHiddenLayers + 1] * sigmoid(layers[countOfHiddenLayers + 1], True)

        for j in range(countOfHiddenLayers, 0, -1):
            error[j] = np.dot(error[j + 1], w[j].T)
            delta[j] = error[j] * sigmoid(layers[j], True)

        for j in range(countOfHiddenLayers, -1, -1):
            w[j] += np.dot(layers[j].T, delta[j + 1])

        if i % 1000 == 0:
            print('Error: ', str(np.mean(np.abs(error[countOfHiddenLayers + 1]))))

            # for i in range(countOfHiddenLayers + 1):
            # for currentW in w[i]:
            # file_weights.write(str(currentW))
            # np.savez_compressed('weights', )
    np.save('weights/weights.npy', w)
    w = None
    w = np.load('weights/weights.npy')

    while True:
        x = np.array([[float(j) for j in input("Enter: ").split()]])

        layers[0] = x

        for j in range(1, countOfHiddenLayers + 2):
            layers[j] = sigmoid(np.dot(layers[j - 1], w[j - 1]))

        print('Answer: ', end='')
        for j in range(outputLayerSize):
            print(float(layers[countOfHiddenLayers + 1][0][j]), end=' ')
        print(end='\n')


if __name__ == '__main__':
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        main()