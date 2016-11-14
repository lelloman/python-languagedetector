#!/usr/bin/python
#coding=UTF-8
'''
(re)train a model on the data stored in DATASET_DIR, each file in the folder corresponds
to a language and must contains only [a-z\s\'] characters
the model is saved after each epoch
'''

from __future__ import print_function
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import Callback
from os import listdir
from os.path import join as path
from random import shuffle, randint
import json
from constants import *
from detector import LanguageDetector, save_model, load_model
import tensorflow as tf

# number of train sentences to generate
# for each language
TRAIN_SIZE = 5000

LOAD_MODEL = 0
BATCH_SIZE = 256

# for each epoch round a new set of training sentences is generated
NB_EPOCH = 3
EPOCH_ROUNDS = 50

# generate a set of languages from the dataset folder
languages = [{'name': x, 'index': i} for i, x in enumerate(listdir(DATASET_DIR))]
json.dump(languages, open(LANGUAGES_JSON_FILENAME, 'w'))
print("languages to learn: ", ', '.join([x['name'] for x in languages]))

# read the dataset file for each language
for lang in languages:
    with open(path(DATASET_DIR, lang['name'])) as f:
        lang['full_text'] = string_to_sequence(f.read())


def make_training_data():
    train = []
    for lang in languages:
        full_text = lang['full_text']
        text_size = len(full_text)
        for _ in range(TRAIN_SIZE):

            # so that a share of the training set will have sentences of length MAX_SENTENCE_LENGTH
            # while another share will be shorter than that and zero-padded
            sample_length = randint(MIN_TRAIN_SAMPLE_LENGTH, MAX_TRAIN_SAMPLE_LENGTH)
            if sample_length > MAX_SENTENCE_LENGTH:
                sample_length = MAX_SENTENCE_LENGTH

            start = randint(0, text_size - sample_length)
            end = start + sample_length
            sentence = full_text[start:end]
            sentence = pad_word(sentence)
            train.append((sentence, lang['index']))
    shuffle(train)

    # one-hot vectors
    X_train = numpy.zeros((TRAIN_SIZE * len(languages), MAX_SENTENCE_LENGTH, 256), dtype=numpy.bool)
    Y_train = numpy.zeros((TRAIN_SIZE * len(languages), len(languages)), dtype=numpy.bool)
    for i, train_sample in enumerate(train):
        word = train_sample[0]
        target = train_sample[1]
        for t, char in enumerate(word):
            X_train[i, t, char] = 1
        Y_train[i, target] = 1

    return X_train, Y_train


def get_model():
    if LOAD_MODEL:
        model = load_model()
    else:
        model = Sequential()
        model.add(LSTM(32, input_shape=(MAX_SENTENCE_LENGTH, 256), return_sequences=True))
        model.add(Dropout(.2))
        model.add(LSTM(16))
        model.add(Dense(len(languages), activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    print(model.summary())
    return model


if __name__ == '__main__':

    # since the network is small, on my computer is faster with cpu
    with tf.device('/cpu:0'):
        model = get_model()

        class EpochCallback(Callback):
            def on_epoch_end(self, epoch, logs={}):
                save_model(model)

        for i in range(EPOCH_ROUNDS):
            print("EPOCH ROUND {} OF {}".format(i+1, EPOCH_ROUNDS))
            X_train, Y_train = make_training_data()
            model.fit(X_train, Y_train, nb_epoch=NB_EPOCH, batch_size=BATCH_SIZE, callbacks=[EpochCallback()])

        detector = LanguageDetector(model=model, languages=languages)
        for t in TEST_TEXTS:
            print(detector.analyze(t)['text'])
