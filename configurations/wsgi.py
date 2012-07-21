from . import importer

importer.install()

try:
    from django.core.wsgi import get_wsgi_application
except ImportError:  # pragma: no cover
    from django.core.handlers.wsgi import WSGIHandler

    def get_wsgi_application():  # noqa
        return WSGIHandler()

# this is just for the crazy ones
application = get_wsgi_application()
