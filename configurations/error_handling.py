from typing import *
from functools import wraps
import sys
import os

from .values import ValueRetrievalError, ValueProcessingError


class TermStyles:
    BOLD = "\033[1m"
    RED = "\033[91m"
    END = "\033[0m"


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
            msg = "{}{}{}".format(TermStyles.RED + TermStyles.BOLD, e, TermStyles.END) \
                if os.isatty(sys.stderr.fileno()) \
                else str(e)
            print(msg, file=sys.stderr)

    return wrapper
