from . import importer

importer.install()

try:
    from django.core.asgi import get_asgi_application
except ImportError:  # pragma: no cover
    from django.core.handlers.asgi import ASGIHandler

    def get_asgi_application():  # noqa
        return ASGIHandler()

# this is just for the crazy ones
application = get_asgi_application()
