# python-languagedetector
A simple machine learning model to recognize languages

The model is really simple and consists of two stacked LSTM layers with a softmax classifier on top. The dataset is quite small and it's composed by 3 texts translated in different languages the texts are "The Universal Declaration of Human Rights", "4 Keys to Hearing God" and dialogues of episode one of Breaking bad.

The idea is, even if we don't actually know a language we might be able to recognize it just by looking at the characters without any conscious reasoning. This method should be much more memory efficient than dictionaries lookup, and also more flexible, it can recognize a language from words that don't even exists! (see 1st test string in [constants.py](https://github.com/lelloman/python-languagedetector/blob/master/constants.py)) 

requires:
- python 2.7 (maybe works with python 3 who knows...)
- keras

The repo contains a trained model, run [detector.py](https://github.com/lelloman/python-languagedetector/blob/master/detector.py) to try it on the tests strings or run [interactive.py](https://github.com/lelloman/python-languagedetector/blob/master/interactive.py) to input the strings yourself. This is a proof of concept but it seems to work quite well, some improvements that should be made are:

- Check the characters encoding, it's been hell and I suspect it's still not ok. The final goal is to use UTF-8 encoded bytearrays.
- Improve the dataset, it seems to work fine but I think it should have samples from many different contexts (chat, laws, novels etc.) and also it could be bigger.
- Accuracy on single words, maybe reduce confidence of prediction if the string is too small.
- Test what the smallest functional model would be, atm it has 40247 parameters, it's still better than having dictionaries but maybe it could be smaller.
- More languages.