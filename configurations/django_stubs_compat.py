"""This file defines a plugin to allow compatibility between configurations and django-stubs."""

from configurations import importer
from mypy.plugin import Options, Plugin


class DjangoStubsCompatPlugin(Plugin):
    """Run the importer install before the django-stubs plugin is imported."""

    def __init__(self, options: Options) -> None:
        """Init the superclass, and install the importer."""
        super().__init__(options)
        importer.install()


def plugin(version) -> DjangoStubsCompatPlugin:
    """Return the plugin."""
    return DjangoStubsCompatPlugin
