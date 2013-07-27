import string
import random

def id_generator(r = 8):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(r))