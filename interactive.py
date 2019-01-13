from detector import *
import tensorflow as tf

with tf.device('/cpu:0'):
    while 1:
        model = load_model()
        user_input = raw_input('write something\n')
        print(analyze_pretty(model, user_input))