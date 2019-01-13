#!/usr/bin/python
# coding=UTF-8

from common import *
import numpy as np


def analyze(model, text):
    text = sanitize_text(text)
    if len(text) > MAX_BYTES_PER_INPUT:
        sentences = []
        for i in range(0, len(text) - MAX_BYTES_PER_INPUT, SENTENCE_OVERLAP):
            end = i + MAX_BYTES_PER_INPUT
            if end > len(text):
                end = len(text)
            sentences.append(text[i: end])
    else:
        sentences = [text]

    percents = [0 for _ in languages]

    # analyze sentences
    for sentence in sentences:

        # make a one-hot vector out of a sentence
        X = np.zeros((1, MAX_BYTES_PER_INPUT, 256, 1), dtype=np.bool)
        padded = pad_input(sentence)
        for t, char in enumerate(padded):
            X[0, t, char] = 1

        # predict the language for one sentence
        prediction = model.predict(X)[0]

        for j, p in enumerate(prediction):
            percents[j] += p

    # average the predictions of all sentences
    for i in range(len(percents)):
        percents[i] /= len(sentences)

    return percents


def analyze_pretty(model, text):
    percents = analyze(model, text)

    # prettify the output string
    predictions = [(lang['name'], percents[i], '|' * int(ROW_WIDTH * percents[i])) for i, lang in
                   enumerate(languages)]
    predictions.sort(key=lambda x: x[1], reverse=True)

    prediction_line = '{{:{}}}{{:.2f}} {{}}'.format(max([len(x['name']) + 2 for x in languages]))
    return '\n"{}"\n'.format(text) + ' '.join([prediction_line.format(*x) for x in predictions])


def predict(model, text):
    percents = analyze(model, text)
    max_index = -1
    max_value = 0
    for i, v in enumerate(percents):
        if v > max_value:
            max_index = i
            max_value = v

    return languages[max_index]['name'] if (max_index > -1 and max_value > .5) else '??'


def print_test_data():
    model = load_model()
    for t in TEST_SENTENCES:
        print(analyze_pretty(model, t))


if __name__ == '__main__':
    print_test_data()
