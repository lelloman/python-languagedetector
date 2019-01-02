from detector import *

while 1:
    model = load_model()
    user_input = raw_input('write something\n')
    print(print_prediction(model, user_input))