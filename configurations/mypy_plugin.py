from mypy.plugin import Options, Plugin

from configurations import importer


class DjangoConfigurationsPlugin(Plugin):
    def __init__(self, options: Options) -> None:
        super().__init__(options)
        # Install settings so that they're available to other
        # mypy plugins called after this one
        importer.install()


def plugin(version: str):
    return DjangoConfigurationsPlugin
