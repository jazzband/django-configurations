try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version

try:
    __version__ = version("django-configurations")
except PackageNotFoundError:
    # package is not installed
    __version__ = None
