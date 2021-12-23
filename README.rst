django-configurations |latest-version|
======================================

|jazzband| |build-status| |codecov| |docs| |python-support| |django-support|

django-configurations eases Django project configuration by relying
on the composability of Python classes. It extends the notion of
Django's module based settings loading with well established
object oriented programming patterns.

Check out the `documentation`_ for more complete examples.

.. |latest-version| image:: https://img.shields.io/pypi/v/django-configurations.svg
   :target: https://pypi.python.org/pypi/django-configurations
   :alt: Latest version on PyPI

.. |jazzband| image:: https://jazzband.co/static/img/badge.svg
   :target: https://jazzband.co/
   :alt: Jazzband

.. |build-status| image:: https://github.com/jazzband/django-configurations/workflows/Test/badge.svg
   :target: https://github.com/jazzband/django-configurations/actions
   :alt: Build Status

.. |codecov| image:: https://codecov.io/github/jazzband/django-configurations/coverage.svg?branch=master
   :target: https://codecov.io/github/jazzband/django-configurations?branch=master
   :alt: Test coverage status

.. |docs| image:: https://img.shields.io/readthedocs/django-configurations/latest.svg
   :target: https://readthedocs.org/projects/django-configurations/
   :alt: Documentation status

.. |python-support| image:: https://img.shields.io/pypi/pyversions/django-configurations.svg
   :target: https://pypi.python.org/pypi/django-configurations
   :alt: Supported Python versions

.. |django-support| image:: https://img.shields.io/pypi/djversions/django-configurations
   :target: https://pypi.org/project/django-configurations
   :alt: Supported Django versions

.. _documentation: https://django-configurations.readthedocs.io/en/latest/

Quickstart
----------

Install django-configurations:

.. code-block:: console

    pip install django-configurations

or, alternatively, if you want to use URL-based values:

.. code-block:: console

    pip install django-configurations[cache,database,email,search]

Then subclass the included ``configurations.Configuration`` class in your
project's **settings.py** or any other module you're using to store the
settings constants, e.g.:

.. code-block:: python

    # mysite/settings.py

    from configurations import Configuration

    class Dev(Configuration):
        DEBUG = True

Set the ``DJANGO_CONFIGURATION`` environment variable to the name of the class
you just created, e.g. in bash:

.. code-block:: console

    export DJANGO_CONFIGURATION=Dev

and the ``DJANGO_SETTINGS_MODULE`` environment variable to the module
import path as usual, e.g. in bash:

.. code-block:: console

    export DJANGO_SETTINGS_MODULE=mysite.settings

*Alternatively* supply the ``--configuration`` option when using Django
management commands along the lines of Django's default ``--settings``
command line option, e.g.

.. code-block:: console

    python manage.py runserver --settings=mysite.settings --configuration=Dev

To enable Django to use your configuration you now have to modify your
**manage.py**, **wsgi.py** or **asgi.py** script to use django-configurations's versions
of the appropriate starter functions, e.g. a typical **manage.py** using
django-configurations would look like this:

.. code-block:: python

    #!/usr/bin/env python

    import os
    import sys

    if __name__ == "__main__":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
        os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

        from configurations.management import execute_from_command_line

        execute_from_command_line(sys.argv)

Notice in line 10 we don't use the common tool
``django.core.management.execute_from_command_line`` but instead
``configurations.management.execute_from_command_line``.

The same applies to your **wsgi.py** file, e.g.:

.. code-block:: python

    import os

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

    from configurations.wsgi import get_wsgi_application

    application = get_wsgi_application()

Here we don't use the default ``django.core.wsgi.get_wsgi_application``
function but instead ``configurations.wsgi.get_wsgi_application``.

Or if you are not serving your app via WSGI but ASGI instead, you need to modify your **asgi.py** file too.:

.. code-block:: python

    import os

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'DEV')

    from configurations.asgi import get_asgi_application

    application = get_asgi_application()

That's it! You can now use your project with ``manage.py`` and your favorite
WSGI/ASGI enabled server.
