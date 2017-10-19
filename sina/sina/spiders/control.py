from functools import wraps
import time
import random

def delay(t):
    if not isinstance(t, int):
        t = 3
    time.sleep(t)
    time.sleep(random.randint(0, 3))
    def wrapfunc(func):
        @wraps(func)
        def inner(*args, **kw):
            return func(*args, **kw)
        return inner
    return wrapfunc