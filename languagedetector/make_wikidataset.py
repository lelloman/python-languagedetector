import wikipedia as wiki
from shutil import rmtree
from os import mkdir
import urllib2
import json
from os.path import join as path
from utils import sanitize_text
from datetime import timedelta

WIKIDATASET_DIR = "wikidataset"
LANGUAGES = [
    "en",
    "de",
    "es",
    "fr",
    "it",
    "pt",
    "nl",

    "sv",
    "pl",
    "vi",
    "ru",
    "uk",
    "fi",
    "hu"
]

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
    rmtree(WIKIDATASET_DIR)
    mkdir(WIKIDATASET_DIR)


def get_titles_from_english(english_title):
    print "get langlinks for title <{}>".format(english_title)
    query = urllib2.urlopen(
        "https://en.wikipedia.org/w/api.php?action=query&titles={}&prop=langlinks&lllimit=500&format=json".format(
            english_title)).read()
    pages = json.loads(query)['query']['pages']
    if len(pages) != 1:
        raise Exception("more than one page per title..?")

    for ele in pages:
        page = pages[ele]
        titles = [{"lang": "en", "*": english_title}] + [
            x for x in page["langlinks"] if x['lang'] in LANGUAGES
        ]
        if len(titles) == len(LANGUAGES):
            return titles
        else:
            raise Exception("found only {} titles".format(len(titles)))


def sanitize_file(filename):
    with open(filename) as f:
        text = f.read()

    with open(filename, 'wb') as f:
        f.write(sanitize_text(text))


if __name__ == "__main__":
    setup_folder()

    print "fetching titles in all languages..."
    titles = [item for title in PAGES_TITLES for item in get_titles_from_english(title)]
    lang_sets = [
        {"lang": lang, "titles": filter(lambda x: x['lang'] == lang, titles)} for lang in LANGUAGES
    ]

    lang_sets = {lang['lang']: [x['*'] for x in lang['titles']] for lang in lang_sets}

    print lang_sets

    wiki.set_rate_limiting(True, timedelta(seconds=1))

    for lang in LANGUAGES:
        wiki.set_lang(lang)
        print lang
        with open(path(WIKIDATASET_DIR, lang), "wb") as f:
            for title in lang_sets[lang]:
                print "\twriting '{}'...".format(title.encode("UTF-8"))
                f.write(wiki.page(title).content.encode("UTF-8") + "\n")

    for lang in LANGUAGES:
        sanitize_file(path(WIKIDATASET_DIR, lang))
    print "DONE"