#!/usr/bin/python
#coding=UTF-8

detector = __import__('detector').LanguageDetector()

while 1:
    print detector.analyze_pretty(raw_input('write something\n'))['text']