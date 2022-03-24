from . import importer
from .errors import with_error_handler

importer.install()

from django.core.wsgi import get_wsgi_application as dj_get_wsgi_application    # noqa: E402

get_wsgi_application = with_error_handler(dj_get_wsgi_application)

# this is just for the crazy ones
application = get_wsgi_application()
