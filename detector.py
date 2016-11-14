#!/usr/bin/python
#coding=UTF-8

from constants import *
import numpy
import json
from keras.models import model_from_json


def load_model(json_filename=MODEL_JSON_FILENAME, weights_filename=MODEL_WEIGHT_FILENAME):
    json_file = open(json_filename, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(weights_filename)
    return model


def save_model(model, json_filename=MODEL_JSON_FILENAME, weights_filename=MODEL_WEIGHT_FILENAME):
    model_json = model.to_json()
    with open(json_filename, "w") as json_file:
        json_file.write(model_json)
    model.save_weights(weights_filename)


class LanguageDetector(object):

    SENTENCE_OVERLAP = 10
    ROW_WIDTH = 30

    def __init__(self, model=None, languages=None):

        if model is None:
            model = load_model()
        if languages is None:
            languages = json.load(open(LANGUAGES_JSON_FILENAME, 'r'))

        self.model = model
        self.languages = languages
        self.prediction_line = '{{:{}}}{{:.2f}} {{}}'.format(max([len(x['name']) + 2 for x in languages]))

    def analyze(self, original_text):
        '''
        cut a string into sentences and analyze them.
        each sentence has a maximum length of MAX_SENTENCE_LENGTH and
        if the original string is longer than that it gets cut into
        sentences by a sliding window which moves by SENTENCE_OVERLAP
        characters steps
        '''

        # remove undesired characters and transform into bytearray
        text = string_to_sequence(original_text)

        # cut sentences
        if len(text) > MAX_SENTENCE_LENGTH:
            sentences = []
            for i in range(0, len(text) - MAX_SENTENCE_LENGTH, self.SENTENCE_OVERLAP):
                end = i + MAX_SENTENCE_LENGTH
                if end > len(text):
                    end = len(text)
                sentences.append(text[i: end])
        else:
            sentences = [text]

        percents = [0 for _ in self.languages]

        # analyze sentences
        for sentence in sentences:

            # make a one-hot vector out of a sentence
            X = numpy.zeros((1, MAX_SENTENCE_LENGTH, 256), dtype=numpy.bool)
            padded = pad_word(sentence)
            for t, char in enumerate(padded):
                X[0, t, char] = 1

            # predict the language for one sentence
            prediction = self.model.predict(X)[0]

            for i, p in enumerate(prediction):
                percents[i] += p

        # average the predictions of all sentences
        for i in range(len(percents)):
            percents[i] /= len(sentences)

        # prettify the output string
        predictions = [(lang['name'], percents[i], '|' * int(self.ROW_WIDTH * percents[i])) for i, lang in
                       enumerate(self.languages)]
        predictions.sort(key=lambda x: x[1], reverse=True)

        return {
            'text': '\n"{}"\n'.format(text) + '\n'.join([self.prediction_line.format(*x) for x in predictions]),
            'percents': percents
        }


if __name__ == '__main__':
    import tensorflow as tf

    with tf.device('/cpu:0'):
        detector = LanguageDetector()
        for t in TEST_TEXTS:
            print(detector.analyze(t)['text'])
