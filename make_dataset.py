from __future__ import print_function
from common import *
from os import mkdir
from shutil import rmtree
from os.path import isdir
from random import shuffle


if isdir(DATA_SET_DIR):
    rmtree(DATA_SET_DIR)

mkdir(DATA_SET_DIR)

languages_names = [x['name'] for x in languages]

for lang in languages_names:
    with open(join_path(WIKI_DATA_SET_DIR, lang)) as f:
        wiki_text = f.read().decode('UTF-8')
    with open(join_path(COMMON_WORDS_DIR, lang)) as f:
        common_words = f.read().decode('UTF-8').split('\n')
    common_words_shuffles = []
    for _ in range(50):
        shuffle(common_words)
        common_words_shuffles.append(' '.join(common_words))
    with open(join_path(DATA_SET_DIR, lang), 'w') as f:
        f.write(wiki_text.encode('UTF-8'))
        f.write(' '.join(common_words_shuffles).encode('UTF-8'))