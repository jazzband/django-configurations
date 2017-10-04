# flake8: noqa
from .base import Configuration
from .decorators import pristinemethod

__version__ = '2.1'
__all__ = ['Configuration', 'pristinemethod']


def _setup():
    from . import importer

    importer.install()

    import django
    django.setup()


def load_ipython_extension(ipython):
    """
    The `ipython` argument is the currently active `InteractiveShell`
    instance, which can be used in any way. This allows you to register
    new magics or aliases, for example.
    """
    _setup()


def setup(app=None):
    """Function used to initialize configurations similar to :func:`.django.setup`."""
    _setup()
