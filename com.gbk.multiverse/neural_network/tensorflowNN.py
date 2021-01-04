import numpy as np
from keras import models, layers

file_tests = open('train/features.txt', 'r')
file_answers = open('train/answers.txt', 'r')

lines_tests = file_tests.read()
tests = [[float(j) for j in line.split()] for line in lines_tests.split('\n')]
file_tests.close()
X = np.array(tests)

lines_answers = file_answers.read()
answers = [[float(j) for j in line.split()] for line in lines_answers.split('\n')]
file_answers.close()
Y = np.array(answers)

model = models.Sequential()
model.add(layers.Dense(30, activation='relu', input_shape=(9,)))
model.add(layers.Dense(40, activation='relu'))
model.add(layers.Dense(30, activation='relu'))
model.add(layers.Dense(5, activation='softmax'))



model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['acc'])
history = model.fit(X, Y, validation_split=0.25, shuffle=True, epochs=50)

#print(model.get_weights())


W = list()
for layer in model.layers:
    weights = layer.get_weights()
    print('*****************')
    #print(weights[0].shape)
    #print(weights)
    W.append(weights)
    print('*****************')
W = np.array(W)
np.save('weights/weightsNN.npy', W)
W = np.load('weights/weightsNN.npy', allow_pickle=True)

for layer in W:
    print('*****************')
    print(layer[0].shape)
    print(layer[0])
    print('*****************')

while True:

    test = np.array([[float(i) for i in input().split()]])
    predicted = model.predict(test)
    print(predicted)