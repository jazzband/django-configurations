from typing import *
from functools import wraps
import sys
import os


class ValueRetrievalError(ValueError):
    """
    Exception is raised when errors occur during the retrieval of a dynamic Value.
    This can happen when the environment variable corresponding to the value is not defined.
    """

    def __init__(self, value_instance: 'configurations.values.Value', error_msg: str) -> None:
        super().__init__(error_msg)
        self.value_instance = value_instance
        self.error_msg = error_msg


class ValueProcessingError(ValueError):
    """
    Exception that is raised when a dynamic Value failed to be processed after retrieval.
    Processing could be i.e. converting from string to a native datatype but also validation.
    """

    def __init__(self, value_instance: 'configurations.values.Value', str_value: str, error_msg: str) -> None:
        super().__init__(error_msg)
        self.value_instance = value_instance
        self.str_value = str_value
        self.error_msg = error_msg


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
