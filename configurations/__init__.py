from .base import Configuration  # noqa
from .decorators import pristinemethod  # noqa
from .version import __version__  # noqa


__all__ = ['Configuration', 'pristinemethod']


def _setup():
    from . import importer

    importer.install()

    from django.apps import apps
    if not apps.ready:
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
