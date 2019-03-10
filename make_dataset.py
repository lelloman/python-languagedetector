from __future__ import print_function
from common import *
from os import mkdir
from shutil import rmtree
from os.path import isdir
from random import shuffle


if isdir(DATA_SET_DIR):
    rmtree(DATA_SET_DIR)

mkdir(DATA_SET_DIR)

for lang in languages_names:
    print(lang)
    with open(join_path(WIKI_DATA_SET_DIR, lang)) as f:
        print("\t reading wiki text...")
        wiki_text = f.read().decode('UTF-8')

    with open(join_path(COMMON_WORDS_DIR, lang)) as f:
        print("\t reading common words...")
        common_words = f.read().decode('UTF-8').split('\n')
    common_words_shuffles = []
    for _ in range(50):
        shuffle(common_words)
        common_words_shuffles.append(' '.join(common_words))

    words_list_file = words_list_files[lang]
    words = []
    if words_list_file is not None:
        file_path = words_list_file.split(' ')[0]
        encoding = words_list_file.split(' ')[1]
        with open(file_path) as f:
            print("\t reading word list...")
            words = f.read().decode(encoding).split('\n')

    with open(join_path(DATA_SET_DIR, lang), 'w') as f:
        print("\t writing dataset entry...")
        f.write(wiki_text.encode('UTF-8'))
        f.write(' '.join(common_words_shuffles).encode('UTF-8'))
        for _ in range(1):
            shuffle(words)
            f.write(' '.join(words).encode('UTF-8'))