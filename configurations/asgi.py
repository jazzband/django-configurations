from . import importer

importer.install()

from django.core.asgi import get_asgi_application  # noqa: E402

# this is just for the crazy ones
application = get_asgi_application()
