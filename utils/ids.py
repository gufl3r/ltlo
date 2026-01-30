import random
import time

def generate_id():
    id_ = int(random.getrandbits(48) - time.time())
    return id_