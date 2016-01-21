# flake8: noqa
from .base import Settings, Configuration
from .decorators import pristinemethod

__version__ = '1.0.1.dev'
__all__ = ['Configuration', 'pristinemethod', 'Settings']


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
    """
    The callback for Sphinx that acts as a Sphinx extension.

    Add ``'configurations'`` to the ``extensions`` config variable
    in your docs' ``conf.py``.
    """
    _setup()
