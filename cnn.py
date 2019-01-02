#!/usr/bin/python
# coding=UTF-8

from __future__ import print_function
from common import *
import numpy
import keras
from keras.callbacks import Callback
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from random import randint


def make_train_data():
    train_data = []
    for index, lang in enumerate(languages):
        full_text = open('dataset/{}'.format(lang['name'])).read()
        text_size = len(full_text)
        for _ in range(TRAIN_SIZE):
            # so that a share of the training set will have sentences of length MAX_SENTENCE_LENGTH
            # while another share will be shorter than that and zero-padded
            sample_length = randint(MIN_TRAIN_SAMPLE_LENGTH, MAX_TRAIN_SAMPLE_LENGTH)
            if sample_length > MAX_BYTES_PER_INPUT:
                sample_length = MAX_BYTES_PER_INPUT

            start = randint(0, text_size - sample_length)
            end = start + sample_length
            sentence = full_text[start:end]
            sentence = pad_input(sentence)
            train_data.append((sentence, index))
        # one-hot vectors

    X_train = numpy.zeros((TRAIN_SIZE * len(languages), MAX_BYTES_PER_INPUT, 256, 1), dtype=numpy.bool)
    Y_train = numpy.zeros((TRAIN_SIZE * len(languages), len(languages)), dtype=numpy.bool)
    for i, train_sample in enumerate(train_data):
        word = train_sample[0]
        target = train_sample[1]
        for t, char in enumerate(word):
            X_train[i, t, char] = 1
        Y_train[i, target] = 1
    return X_train, Y_train


def make_model():
    input_shape = MAX_BYTES_PER_INPUT, 256, 1
    num_classes = len(languages)

    model = Sequential()
    model.add(Conv2D(256, (2, 256), padding='valid', input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(Conv2D(128, (5, 1), padding='valid'))
    model.add(Activation('relu'))
    # model.add(Conv2D(64, (3, 1), padding='valid'))
    # model.add(Activation('relu'))

    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(num_classes * 2))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    # initiate RMSprop optimizer
    opt = keras.optimizers.rmsprop(lr=0.001, decay=1e-9)
    # opt = keras.optimizers.adagrad(lr = 0.001)

    # Let's train the model using RMSprop
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])
    return model


model = make_model()
X_train, Y_train = make_train_data()

print(model.summary())


class EpochCallback(Callback):
    def on_epoch_end(self, epoch, logs={}):
        save_model(model)

model.fit(X_train, Y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=[EpochCallback()])


