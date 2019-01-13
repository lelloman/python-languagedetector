from __future__ import print_function
from detector import *
from os import listdir
from sys import stdout
import tensorflow as tf

model = load_model()

validation_entries = []

for lang in listdir(VALIDATION_SET_DIR):
    with open(join_path(VALIDATION_SET_DIR, lang), 'r') as f:
        sentences = f.read().split('\n')
        for sentence in sentences:
            if sentence:
                validation_entries.append((lang, sentence))


validation_results = {
    lang['name'] : {
        'tested': 0,
        'passed': 0
    }
    for lang in languages
}

i = 0
for lang, text in validation_entries:
    print('{:.1f}'.format(100. * i / len(validation_entries)), end='\r')
    stdout.flush()
    i += 1
    result = validation_results[lang]
    result['tested'] += 1
    predicted = predict(model, text)
    if lang != predicted:
        print(lang, 'predicted as', predicted, 'for "{}"'.format(text))
    else:
        result['passed'] += 1

print("\nResult:")
total_tested, total_passed = 0, 0
for key, value in sorted(validation_results.items(), key=lambda x: x[0]):
    tested = value['tested']
    total_tested += tested
    passed = value['passed']
    total_passed += passed
    print("{}: {}/{}".format(key, passed, tested))

print("total: {}/{} -> {:.2f}%".format(total_passed, total_tested, 100 * float(total_passed) / total_tested))