# python-languagedetector
A simple machine learning model to recognize languages.

The idea here is that even if we don't actually know a language we might be able to recognize it just by looking at the characters without any conscious reasoning. This method should be much more memory efficient than using dictionaries, and also more flexible, it can recognize a language from words that don't even exists!

The model consists of a few convolutional layers with a softmax classifier on top. The dataset is generated from wikipedia pages, they can be downloaded by running [make_wiki_dataset.py](https://github.com/lelloman/python-languagedetector/blob/master/make_wiki_dataset.py).

requires:
- python 3
- tensorflow
- keras
- wikipedia
- beautifulsoup
- feedparser

In order to have a working model run:
- [make_wiki_dataset.py](https://github.com/lelloman/python-languagedetector/blob/master/make_wiki_dataset.py), downloads the wiki pages for each language and create a file for each language in `wikidataset` directory, all files needs to be copied to `dataset` manually -_-'.
- [train.py](https://github.com/lelloman/python-languagedetector/blob/master/train.py), performs the training of a model. There is a variable `LOAD_MODEL` in the script that can be set so that the training can be continued from a previous model, by default it's false and new parameters will be created on each run.
- [make_validation_set.py](https://github.com/lelloman/python-languagedetector/blob/master/make_validation_set.py), downloads news feeds for each language into `validationset` directory.
- [validate.py](https://github.com/lelloman/python-languagedetector/blob/master/validate.py) loads the trained model and preforms prediction for all the entries in `validationset`, the accuracy should be > 95%.
- [interactive.py](https://github.com/lelloman/python-languagedetector/blob/master/interactive.py) makes predictions for inputs provided via command line.

The trained model can also be exported as TensorflowLite format with [to_tensorflow_lite.py](https://github.com/lelloman/python-languagedetector/blob/master/to_tensorflow_lite.py). An Android implementation that runs the TensorflowLite model is also available [here](https://github.com/lelloman/android-language-detector)

Run with docker image `docker run --gpus all -v /path/to/project/on/host:/languagedetector -it tensorflow/tensorflow:latest-gpu bash`