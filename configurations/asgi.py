from . import importer

importer.install()

from django.core.asgi import get_asgi_application

# this is just for the crazy ones
application = get_asgi_application()
