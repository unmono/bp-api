import functools
import time
from typing import Callable


def execution_timer(func: Callable, n: int = 1) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = None
        for _ in range(n):
            result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'Execution time: {end - start}')
        return result

    return wrapper
