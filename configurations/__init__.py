# flake8: noqa
from .base import Settings, Configuration
from .decorators import pristinemethod

__version__ = '0.8'
__all__ = ['Configuration', 'pristinemethod', 'Settings']


def load_ipython_extension(ipython):
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example.
    from . import importer

    importer.install()
