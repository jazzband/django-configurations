from . import importer
from .errors import with_error_handler

importer.install()

from django.core.asgi import get_asgi_application as dj_get_asgi_application  # noqa: E402

get_asgi_application = with_error_handler(dj_get_asgi_application)

# this is just for the crazy ones
application = get_asgi_application()
