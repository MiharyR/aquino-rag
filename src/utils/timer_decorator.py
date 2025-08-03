import time
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO, format='%(message)s')


def timer(func):
    """Decorator to log the execution time of a function"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f'start - {func.__name__}')
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        logging.info(f'end   - {func.__name__} : {duration:.2f}s')
        return result

    return wrapper


# Décorateur de classe
def decorate_all_methods(decorator: callable = timer):
    """Decorator to apply a decorator to all methods of a class"""

    def decorate(cls):
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                setattr(cls, attr_name, decorator(attr_value))
        return cls

    return decorate
