"""
this is debugging code created by kai to decorate code and get an idea of how fast the code was running
"""

from time import time

def stop_watch(func):
    # This tells you how long it took for a function to execute.
    def wrap_func(*args, **kwargs):
        t1 = time()
        result = func(*args, **kwargs)
        t2 = time()
        print(f'Function {func.__name__!r} executed in {(t2 - t1):.4f}s')
        return result

    return wrap_func