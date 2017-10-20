#!/usr/bin/python

from constants import TEST_TEXTS
from detector import LanguageDetector as Detector

def test():
    detector = Detector()
    for test in TEST_TEXTS:
        print detector.analyze(test)['text']


if __name__ == '__main__':
    test()