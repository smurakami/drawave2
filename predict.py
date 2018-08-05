import numpy as np
import cv2
import matplotlib.pyplot as plt
import json

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D


num_classes = 12

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu',
                 input_shape=(28, 28, 1)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

model.load_weights('./models/weights.19-0.61-0.79-0.51-0.82.hdf5')

def predict(paths):
    image = np.zeros((640, 640))

    for path in paths:
        if path['mode'] == 'draw':
            color = (1, 1, 1)
            thickness = 32
        else:
            color = (0, 0, 0)
            thickness = 16

        data = path['data']
        for a, b in zip(data, data[1:]):
            a = tuple(map(int, a))
            b = tuple(map(int, b))
                
            image = cv2.line(image, a, b, color, thickness)
        

    resized = cv2.resize(image, (28, 28), interpolation=cv2.INTER_AREA)

    data_input = resized.reshape((1, 28, 28, 1))
    data_input = data_input * 2 - 1

    return model.predict(data_input)







