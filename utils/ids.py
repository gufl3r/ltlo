import random
import time

def generate_id():
    raw = (
        time.process_time_ns()
        * time.perf_counter()
        * random.random()
    )

    id_ = int(raw) % 10**13
    return id_