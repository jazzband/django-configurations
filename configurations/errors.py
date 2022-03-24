from typing import *
from functools import wraps
import sys
import os

if TYPE_CHECKING:
    from .values import Value


class TermStyles:
    BOLD = "\033[1m" if os.isatty(sys.stderr.fileno()) else ""
    RED = "\033[91m" if os.isatty(sys.stderr.fileno()) else ""
    END = "\033[0m" if os.isatty(sys.stderr.fileno()) else ""


class ConfigurationError(ValueError):
    """
    Base error class that is used to indicate that something went wrong during configuration.

    This error type (and subclasses) is caught and pretty-printed by django-configurations so that an end-user does not
    see an unwieldy traceback but instead a helpful error message.
    """

    def __init__(self, main_error_msg: str, explanation_lines: List[str]) -> None:
        """
        :param main_error_msg: Main message that describes the error.
            This will be displayed before all *explanation_lines* and in the traceback (although tracebacks are normally
            not rendered)
        :param explanation_lines: Additional lines of explanations which further describe the error or give hints on
            how to fix it.
        """
        super().__init__(main_error_msg)
        self.main_error_msg = main_error_msg
        self.explanation_lines = explanation_lines


class ValueRetrievalError(ConfigurationError):
    """
    Exception that is raised when errors occur during the retrieval of a Value by one of the `Value` classes.
    This can happen when the environment variable corresponding to the value is not defined.
    """

    def __init__(self, value_instance: "Value", *extra_explanation_lines: str):
        """
        :param value_instance: The `Value` instance which caused the generation of this error
        :param extra_explanation_lines: Extra lines that will be appended to `ConfigurationError.explanation_lines`
            in addition the ones automatically generated from the provided *value_instance*.
        """
        explanation_lines = list(extra_explanation_lines)
        if value_instance.destination_name is not None:
            explanation_lines.append(f"{value_instance.destination_name} is taken from the environment variable "
                                     f"{value_instance.full_environ_name} as a {type(value_instance).__name__}")

        super().__init__(
            f"Value of {value_instance.destination_name} could not be retrieved from environment",
            explanation_lines
        )


class ValueProcessingError(ConfigurationError):
    """
    Exception that is raised when a dynamic Value failed to be processed by one of the `Value` classes after retrieval.

    Processing could be i.e. converting from string to a native datatype or validation.
    """

    def __init__(self, value_instance: "Value", raw_value: str, *extra_explanation_lines: str):
        """
        :param value_instance: The `Value` instance which caused the generation of this error
        :param raw_value: The raw value that was retrieved from the environment and which could not be processed further
        :param extra_explanation_lines: Extra lines that will be prepended to `ConfigurationError.explanation_lines`
            in addition the ones automatically generated from the provided *value_instance*.
        """
        error = f"{value_instance.destination_name} was given an invalid value"
        if hasattr(value_instance, "message"):
            error += ": " + value_instance.message.format(raw_value)

        explanation_lines = list(extra_explanation_lines)
        if value_instance.destination_name is not None:
            explanation_lines.append(f"{value_instance.destination_name} is taken from the environment variable "
                                     f"{value_instance.full_environ_name} as a {type(value_instance).__name__}")

        explanation_lines.append(f"'{raw_value}' was received but that is invalid")

        super().__init__(error, explanation_lines)


def with_error_handler(callee: Callable) -> Callable:
    """
    A decorator which is designed to wrap django entry points with an error handler so that django-configuration
    originated errors can be caught and rendered to the user in a readable format.
    """

    @wraps(callee)
    def wrapper(*args, **kwargs):
        try:
            return callee(*args, **kwargs)
        except ConfigurationError as e:
            msg = "{}{}{}".format(TermStyles.RED + TermStyles.BOLD, e, TermStyles.END)
            for line in e.explanation_lines:
                msg += f"\n    {line}"
            print(msg, file=sys.stderr)

    return wrapper
