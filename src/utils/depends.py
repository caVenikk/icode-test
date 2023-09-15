from typing import Callable


def depends(dependency_func: Callable):
    def wrapper(*args, **kwargs):
        result = dependency_func(*args, **kwargs)
        return result

    return wrapper
