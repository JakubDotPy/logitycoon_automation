import functools
import random
import time


def random_delay(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        delay = random.randint(8, 15) / 10
        time.sleep(delay)
        return func(*args, **kwargs)

    return wrapper
