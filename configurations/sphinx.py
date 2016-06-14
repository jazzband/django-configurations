from . import _setup, __version__


def setup(app=None):
    """
    The callback for Sphinx that acts as a Sphinx extension.

    Add ``'configurations'`` to the ``extensions`` config variable
    in your docs' ``conf.py``.
    """
    _setup()
    return {'version': __version__, 'parallel_read_safe': True}
