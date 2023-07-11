import functools
import random
import time
from enum import Enum


class City(Enum):
    PILSEN = 63


def random_delay(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        delay = random.randint(8, 15) / 10
        time.sleep(delay)
        return func(*args, **kwargs)

    return wrapper
