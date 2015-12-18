django-configurations
=====================

.. image:: https://travis-ci.org/jazzband/django-configurations.svg?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/jazzband/django-configurations

.. image:: https://jazzband.co/static/img/badge.svg
   :alt: Jazzband
   :target: https://jazzband.co/

django-configurations eases Django project configuration by relying
on the composability of Python classes. It extends the notion of
Django's module based settings loading with well established
object oriented programming patterns.

Check out the `documentation`__ for more complete examples.

.. __: http://django-configurations.readthedocs.org/en/latest/


Quickstart
----------

Install django-configurations:

.. code-block:: console

    pip install django-configurations

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
command line option, e.g.::

    python manage.py runserver --settings=mysite.settings --configuration=Dev

To enable Django to use your configuration you now have to modify your
**manage.py** or **wsgi.py** script to use django-configurations's versions
of the appropriate starter functions, e.g. a typical **manage.py** using
django-configurations would look like this:

.. code-block:: python
   :emphasize-lines: 10

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
   :emphasize-lines: 6

    import os

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

    from configurations.wsgi import get_wsgi_application

    application = get_wsgi_application()

Here we don't use the default ``django.core.wsgi.get_wsgi_application``
function but instead ``configurations.wsgi.get_wsgi_application``.

That's it! You can now use your project with ``manage.py`` and your favorite
WSGI enabled server.
