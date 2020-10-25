#!/usr/bin/python
# coding=UTF-8
import wikipedia as wiki
from shutil import rmtree
from os import mkdir
import urllib
import json
from os.path import join as path, isdir
from common import sanitize_text, languages
from datetime import timedelta

language_names = [x['name'] for x in languages]

WIKIDATASET_DIR_RAW = "wikidataset_raw"
PAGES_TITLES = [
    "Agriculture",
    "History",
    "Literature",
    "Rome",
    "Paris",
    "Berlin",
    "London",
    "Lisbon",
    "Amsterdam",
    "Madrid",
    "Internet",
    "Education",
    "Music",
    "Wheel",
    "Fire",
    "Sea",
    "Earth"
]


def setup_folder():
    if isdir(WIKIDATASET_DIR_RAW):
        rmtree(WIKIDATASET_DIR_RAW)
    mkdir(WIKIDATASET_DIR_RAW)


def get_titles_from_english(english_title):
    print("get langlinks for title <{}>".format(english_title))
    query = urllib.request.urlopen(
        "https://en.wikipedia.org/w/api.php?action=query&titles={}&prop=langlinks&lllimit=500&format=json".format(
            english_title)).read()
    pages = json.loads(query)['query']['pages']
    if len(pages) != 1:
        raise Exception("more than one page per title..?")

    for ele in pages:
        page = pages[ele]
        titles = [{"lang": "en", "*": english_title}]
        langlinks = page['langlinks']
        for lang in [x for x in language_names if x != 'en']:
            filtered = list(filter(lambda x: x['lang'] == lang, langlinks))
            if filtered:
                titles.append(filtered[0])
            else:
                print("Didnt find page title '{}' for {}".format(english_title, lang))

        return titles


def sanitize_file(filename):
    with open(filename) as f:
        text = f.read()

    with open(filename, 'wb') as f:
        f.write(sanitize_text(text))


def download_raw_wiki_dataset():
    if isdir(WIKIDATASET_DIR_RAW) and input("Raw wiki dataset already exists, do you want to erase it and re-download "
                                            "the enitre thing? Y/N").strip().lower() == "y":
        rmtree(WIKIDATASET_DIR_RAW)
        mkdir(WIKIDATASET_DIR_RAW)

        print("fetching titles in all languages...")
        titles = [item for title in PAGES_TITLES for item in get_titles_from_english(title)]
        lang_sets = [
            {"lang": lang, "titles": [x for x in titles if x['lang'] == lang]} for lang in language_names
        ]

        lang_sets = {lang['lang']: [x['*'] for x in lang['titles']] for lang in lang_sets}
        print(lang_sets)

        for lang in language_names:
            wiki.set_lang(lang)
            print(lang)
            with open(path(WIKIDATASET_DIR_RAW, lang + "_raw"), "wb") as f:
                for title in lang_sets[lang]:
                    print("\twriting '{}'...".format(title))
                    try:
                        f.write((wiki.page(title).content + "\n").encode("UTF-8"))
                    except Exception as e:
                        print(e)
    else:
        print("Skipped raw wiki dataset download")


def make_dataset():
    if isdir("dataset"):
        rmtree("dataset")

    mkdir("dataset")

    for lang in language_names:
        raw_lang_file_name = path(WIKIDATASET_DIR_RAW, lang + "_raw")
        with open(raw_lang_file_name, "r") as f:
            raw_text = f.read()
            sanitized = sanitize_text(raw_text)
            with open(path("dataset", lang), "w") as wf:
                wf.write(sanitized)


if __name__ == "__main__":
    wiki.set_rate_limiting(True, timedelta(seconds=0.01))

    # download_raw_wiki_dataset()

    make_dataset()
    print("DONE")
