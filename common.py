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

MAX_BYTES_PER_INPUT = 20
SENTENCE_OVERLAP = 10

ROW_WIDTH = 20

MODEL_JSON_FILENAME = 'model_{}.json'
WEIGHTS_FILENAME = 'weights_{}.h5'

GROUP_DETECTOR_MODEL_NAME = "group"

languages_names = [
    'da',
    'de',
    'en',
    'es',
    'fi',
    'fr',
    'hu',
    'it',
    # 'ja',
    'nl',
    'no',
    'pl',
    'pt',
    'ro',
    'ru',
    'sv',
    'uk',
    # 'vi'
]

languages_groups_names = [
    'da',
    'de',
    'en',
    'es',
    'fi',
    'fr',
    'hu',
    'it',
    # 'ja',
    'nl',
    'no',
    'pl',
    'pt',
    'ro',
    'ru',
    'sv',
    'uk',
    # 'vi'
]

# http://ftp.gnu.org/gnu/aspell/dict/
words_list_files = {
    'da': '/usr/share/dict/danish UTF-8',
    'de': '/usr/share/dict/ngerman UTF-8',
    'en': '/usr/share/dict/american-english UTF-8',
    'es': '/usr/share/dict/spanish UTF-8',
    'fi': None,
    'fr': '/usr/share/dict/french UTF-8',
    'hu': '/home/lelloman/PycharmProjects/python-languagedetector/hu UTF-8',
    'it': '/usr/share/dict/italian UTF-8',
    'ja': None,
    'nl': '/usr/share/dict/dutch UTF-8',
    'no': '/usr/share/dict/nynorsk ISO-8859-1',
    'pl': '/home/lelloman/PycharmProjects/python-languagedetector/pl UTF-8',
    'pt': '/usr/share/dict/portuguese UTF-8',
    'ro': '/home/lelloman/PycharmProjects/python-languagedetector/ro UTF-8',
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

groups = []
for i, group_name in enumerate(languages_groups_names):
    groups.append({
        'name': group_name,
        'index': i,
        'lang_names': group_name.split('-')
    })

language_group_indices = {}
for lang in languages_names:
    print("asd", lang)
    language_group_indices[lang] = [group['index'] for group in groups if lang in group['lang_names']][0]

print(len(languages), 'languages:', ', '.join(name for name in languages_names))
print(len(groups), 'groups:', ', '.join(group['name'] for group in groups))
print('language_troup_indices', language_group_indices)


def load_model(name):
    json_file = open(MODEL_JSON_FILENAME.format(name), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(WEIGHTS_FILENAME.format(name))
    return model


def save_model(model, name):
    model_json = model.to_json()
    with open(MODEL_JSON_FILENAME.format(name), "w") as json_file:
        json_file.write(model_json)
    model.save_weights(WEIGHTS_FILENAME.format(name))


def pad_input(word):
    out = bytearray(MAX_BYTES_PER_INPUT)
    out[MAX_BYTES_PER_INPUT - len(word):] = word
    return out


def sanitize_text(original_text):
    original_text = original_text
    text = re.sub("\s\s+", " ", original_text.lower())
    text = re.sub('[=><\n\t:\-,.0-9"«»…„“]', "", text)
    return text


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)
