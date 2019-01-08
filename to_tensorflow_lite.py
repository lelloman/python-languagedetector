#!/usr/bin/python
from __future__ import print_function
from common import  *
import tensorflow.contrib.lite as tflite

import keras

a = keras.models.Sequential()

model = load_model()

full_model_file_name = 'full_model.h5'
model.save(full_model_file_name)
converter = tflite.TFLiteConverter.from_keras_model_file(full_model_file_name)
tflite_model = converter.convert()
open("converted_model.tflite", "wb").write(tflite_model)