from __future__ import print_function
from common import *
from os.path import join as join_path, isdir
from shutil import rmtree
from os import mkdir, sep
import feedparser
from bs4 import BeautifulSoup as bs

languages_names = [x['name'] for x in languages]

rss_sources = {
    'da': [
        'https://politiken.dk/rss/senestenyt.rss',
        'https://borsen.dk/rss/'
    ],
    'de': [
        'http://www.spiegel.de/index.rss',
        'https://www.faz.net/rss/aktuell/'
    ],
    'en': [
        'http://feeds.washingtonpost.com/rss/rss_powerpost',
        'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
    ],
    'es': [
        'http://ep00.epimg.net/rss/elpais/portada.xml',
        'https://e00-elmundo.uecdn.es/elmundo/rss/espana.xml'
    ],
    'fi': [
        'https://www.iltalehti.fi/rss/uutiset.xml',
        'https://www.uusisuomi.fi/raha/feed'
    ],
    'fr': [
        'https://www.lemonde.fr/rss/une.xml',
        'http://www.lefigaro.fr/rss/figaro_flash-actu.xml'
    ],
    'hu': [
        'https://nepszava.hu/feed',
        'https://www.vg.hu/feed/'
    ],
    'it': [
        'https://www.fanpage.it/feed/',
        'http://www.ansa.it/campania/notizie/campania_rss.xml'
    ],
    'ja': [
        'http://feeds.cnn.co.jp/rss/cnn/cnn.rdf',
        'https://thebridge.jp/feed'
    ],
    'nl': [
        'https://www.telegraaf.nl/rss',
        'https://www.ad.nl/nieuws/rss.xml'
    ],
    'no': [
        'https://www.vg.no/rss/feed/forsiden/?format=rss',
        'https://www.aftenposten.no/rss'
    ],
    'pl': [
        'http://rss.gazeta.pl/pub/rss/najnowsze_wyborcza.xml',
        'https://www.rp.pl/rss/1019'
    ],
    'pt': [
        'https://feeds.folha.uol.com.br/emcimadahora/rss091.xml',
        'http://feeds.jn.pt/JN-Nacional'
    ],
    'ro': [
        'https://evz.ro/rss.xml',
        'https://adevarul.ro/rss/'
    ],
    'ru': [
        'https://www.mk.ru/rss/index.xml',
        'https://iz.ru/xml/rss/all.xml'
    ],
    'sv': [
        'https://www.di.se/rss',
        'https://www.arbetarbladet.se/feed'
    ],
    'uk': [
        'https://ukurier.gov.ua/uk/feed/',
        'http://day.kyiv.ua/uk/news-rss.xml'
    ],
    'vi': [
        'https://vnexpress.net/rss/tin-moi-nhat.rss',
        'https://www.tienphong.vn/rss/ho-chi-minh-288.rss'
    ]
}


def text_from_html(html):
    return bs(html, "lxml").text


def make_validation_set():
    if isdir(VALIDATION_SET_DIR):
        user_input = raw_input("Validation set directory already exists, should delete it and re-fetch the data? Y/N\n")
        if user_input.lower() != 'y':
            print("Nothing to do.")
            exit(0)
        else:
            print("Deleting old validate set dir", VALIDATION_SET_DIR)
            rmtree(VALIDATION_SET_DIR)

    print("Creating new directory", VALIDATION_SET_DIR)
    mkdir(VALIDATION_SET_DIR)

    # for lang in ['ja']:
    for lang in languages_names:
        print(lang)
        if lang not in rss_sources:
            print("\tSkipping", lang, "as there are no sources.")
            continue

        with open(join_path(VALIDATION_SET_DIR, lang), 'w') as f:
            for source in rss_sources[lang]:
                feed = feedparser.parse(source)
                items = feed.entries
                for item in items:
                    title = text_from_html(item['title'])
                    summary = text_from_html(item['summary'])
                    validation_text = sanitize_text(title) + ' ' + sanitize_text(summary)
                    if len(validation_text) > 200:
                        validation_text = validation_text[:200]
                    f.write(validation_text.encode("UTF-8"))
                    f.write('\n')
                    # print('\t', title, ' -> ', summary, ' -> ', validation_text)
                print("\tfound", len(items), "feeds in", source)


if __name__ == '__main__':
    make_validation_set()