#!/usr/bin/python
# coding=UTF-8
from __future__ import print_function
import numpy as np
import re
from keras.models import model_from_json
from os import sep
from os.path import join as join_path

THIS_FILE_DIR = sep.join(__file__.split(sep)[:-1])
VALIDATION_SET_DIR = join_path(THIS_FILE_DIR, 'validationset')
COMMON_WORDS_DIR = join_path(THIS_FILE_DIR, 'commonwords')
WIKI_DATA_SET_DIR = join_path(THIS_FILE_DIR, 'wikidataset')
DATA_SET_DIR = join_path(THIS_FILE_DIR, 'dataset')

MAX_BYTES_PER_INPUT = 36
SENTENCE_OVERLAP = 24

ROW_WIDTH = 20

MODEL_JSON_FILENAME = 'model.json'
WEIGHTS_FILENAME = 'weights.h5'

languages_names = [
    #'da',
    #'de',
    #'en',
    'es',
    #'fi',
    #'fr',
    #'hu',
    'it',
    #'ja',
    #'nl',
    #'no',
    #'pl',
    'pt',
    #'ro',
    #'ru',
    #'sv',
    #'uk',
    #'vi'
]

words_list_files = {
    'da': '/usr/share/dict/danish UTF-8',
    'de': '/usr/share/dict/ngerman UTF-8',
    'en': '/usr/share/dict/american-english UTF-8',
    'es': '/usr/share/dict/spanish UTF-8',
    'fi': None,
    'fr': '/usr/share/dict/french UTF-8',
    'hu': None,
    'it': '/usr/share/dict/italian UTF-8',
    'ja': None,
    'nl': '/usr/share/dict/dutch UTF-8',
    'no': '/usr/share/dict/nynorsk ISO-8859-1',
    'pl': None,
    'pt': '/usr/share/dict/portuguese UTF-8',
    'ro': None,
    'ru': None,
    'sv': '/usr/share/dict/swedish ISO-8859-1',
    'uk': '/usr/share/dict/ukrainian UTF-8',
    'vi': None,
}

languages = [
    {
        'name': unicode(x),
        'index': i
    } for i, x in enumerate(languages_names)
]
print(len(languages), 'languages:', ','.join(language['name'] for language in languages))


def load_model():
    json_file = open(MODEL_JSON_FILENAME, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(WEIGHTS_FILENAME)
    return model


def save_model(model):
    model_json = model.to_json()
    with open(MODEL_JSON_FILENAME, "w") as json_file:
        json_file.write(model_json)
    model.save_weights(WEIGHTS_FILENAME)


def pad_input(word):
    out = bytearray(MAX_BYTES_PER_INPUT)
    out[MAX_BYTES_PER_INPUT - len(word):] = word
    return out


def sanitize_text(original_text):
    original_text = original_text
    text = re.sub("\s\s+", " ", original_text.lower())
    for ele in ['=', '>', '<', '"', '\t', '\n', "'"]:
        text = text.replace(ele, "")
    return text


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)
