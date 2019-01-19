#!/usr/bin/python
# coding=UTF-8

from __future__ import print_function
from common import *
import numpy
import keras
from keras.callbacks import Callback
from keras.models import Sequential
from keras.layers import *
from random import randint
from os.path import isdir
from make_validation_set import make_validation_set
from random import shuffle


LOAD_MODEL = 0
MIN_TRAIN_SAMPLE_LENGTH = MAX_BYTES_PER_INPUT / 2
MAX_TRAIN_SAMPLE_LENGTH = MAX_BYTES_PER_INPUT * 2

TRAIN_SIZE = 1000
EPOCHS_ROUND = 20
EPOCHS_PER_TRAINING_SET = 1
BATCH_SIZE = 500


def make_train_data():
    train_data = []
    for lang in languages_names:
        full_text = open('dataset/{}'.format(lang)).read()
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
            index = language_group_indices[lang]
            train_data.append((sentence, index))

    # one-hot vectors
    X_train = numpy.zeros((TRAIN_SIZE * len(languages), MAX_BYTES_PER_INPUT, 256, 1), dtype=numpy.bool)
    Y_train = numpy.zeros((TRAIN_SIZE * len(languages), len(groups)), dtype=numpy.bool)
    for i, train_sample in enumerate(train_data):
        word = train_sample[0]
        target = train_sample[1]
        for t, char in enumerate(word):
            X_train[i, t, char] = 1
        Y_train[i, target] = 1
    return X_train, Y_train


def load_validation_set():
    if not isdir(VALIDATION_SET_DIR):
        answer = raw_input('Validation set dir does not exist, do you want to create the validation set?Y/n\n')
        if answer.lower() == 'y':
            make_validation_set()
        else:
            return []

    data = []
    for lang in languages:
        with open(join_path(VALIDATION_SET_DIR, lang['name'])) as f:
            sentences = [sanitize_text(x) for x in f.read().split('\n')]
            for sentence in sentences:
                for i in range(0, len(sentence) - MAX_BYTES_PER_INPUT, SENTENCE_OVERLAP):
                    sub_sentence = pad_input(sentence[i: min(len(sentence), i + MAX_BYTES_PER_INPUT)])
                    data.append((language_group_indices[lang['name']], sub_sentence))

    return data


def make_model():
    input_shape = MAX_BYTES_PER_INPUT, 256, 1
    num_classes = len(groups)

    model = Sequential()
    first_conv_channels = 192
    second_conv_channels = 192
    third_conv_channels = 32

    model.add(Conv2D(first_conv_channels, (2, 256), strides=1, padding='valid', input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(BatchNormalization())

    model.add(Conv2D(second_conv_channels, (2, 1), strides=2, padding='valid', input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(BatchNormalization())

    model.add(MaxPooling2D(pool_size=(2, 1)))

    model.add(Conv2D(third_conv_channels, (2, 1), strides=2, padding='valid', input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(BatchNormalization())

    model.add(Reshape(target_shape=(4, 32)))

    model.add(LSTM(num_classes * 3, return_sequences=True))
    model.add(BatchNormalization())

    model.add(Dropout(0.333))
    model.add(LSTM(num_classes * 2, return_sequences=False))

    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))
    return model


def get_model():
    if LOAD_MODEL:
        return load_model(GROUP_DETECTOR_MODEL_NAME)
    else:
        return make_model()


def train_group_detector():
    model = get_model()
    opt = keras.optimizers.rmsprop(lr=0.0001, decay=0.00001)
    # opt = keras.optimizers.adagrad(lr = 0.0001)

    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])
    print(model.summary())

    validation_set = load_validation_set()
    validation_data_size = len(validation_set)

    class EpochCallback(Callback):
        def on_epoch_end(self, epoch, logs=None):
            save_model(model, GROUP_DETECTOR_MODEL_NAME)

    X_validation = numpy.zeros((validation_data_size, MAX_BYTES_PER_INPUT, 256, 1), dtype=numpy.bool)
    Y_validation = numpy.zeros((validation_data_size, len(groups)), dtype=numpy.bool)
    for i, validation_sample in enumerate(validation_set[:validation_data_size]):
        word = validation_sample[1]
        target = validation_sample[0]
        for t, char in enumerate(word):
            X_validation[i, t, char] = 1
            Y_validation[i, target] = 1

    for epoch_round in range(EPOCHS_ROUND):
        print('{}/{}'.format(epoch_round + 1, EPOCHS_ROUND))
        X_train, Y_train = make_train_data()
        model.fit(X_train, Y_train, epochs=EPOCHS_PER_TRAINING_SET, batch_size=BATCH_SIZE, callbacks=[EpochCallback()],
                  validation_data=(X_validation, Y_validation))


if __name__ == '__main__':
    train_group_detector()
