from . import importer

importer.install()

from django.core.servers.fastcgi import runfastcgi  # noqa
