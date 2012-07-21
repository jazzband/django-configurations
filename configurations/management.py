from . import importer

importer.install()

from django.core.management import execute_from_command_line  # noqa
