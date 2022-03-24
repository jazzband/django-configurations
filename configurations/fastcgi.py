from . import importer
from .errors import with_error_handler

importer.install()

from django.core.servers.fastcgi import dj_runfastcgi  # noqa

runfastcgi = with_error_handler(dj_runfastcgi)
