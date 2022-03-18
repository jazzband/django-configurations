from typing import *
from functools import wraps
import sys

from .values import ValueRetrievalError, ValueProcessingError


def with_error_handler(callee: Callable) -> Callable:
    """
    A decorator which is designed to wrap django entry points with an error handler so that django-configuration
    originated errors can be caught and rendered to the user in a readable format.
    """
    @wraps(callee)
    def wrapper(*args, **kwargs):
        try:
            return callee(*args, **kwargs)
        except (ValueRetrievalError, ValueProcessingError) as e:
            print(e, file=sys.stderr)

    return wrapper
