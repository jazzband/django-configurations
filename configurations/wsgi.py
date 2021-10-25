from . import importer

importer.install()

from django.core.wsgi import get_wsgi_application    # noqa: E402

# this is just for the crazy ones
application = get_wsgi_application()
