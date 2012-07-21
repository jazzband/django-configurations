django-configurations
=====================

.. image:: https://secure.travis-ci.org/jezdez/django-configurations.png
   :alt: Build Status
   :target: https://secure.travis-ci.org/jezdez/django-configurations

django-configurations eases Django project configuration by relying
on the composability of Python classes. It extends the notion of
Django's module based settings loading with well established
object oriented programming patterns.

Quickstart
----------

Install django-configurations::

    pip install django-configurations

Then subclass the included ``configurations.Settings`` class in your
project's ``settings.py`` or any other module you're using to store the
settings constants, e.g.::

    from configurations import Settings

    class MySiteSettings(Settings):
        DEBUG = True

Set the ``DJANGO_CONFIGURATION`` environment variable to the name of the class
you just created, e.g. in bash::

    export DJANGO_CONFIGURATION=MySettings

and the ``DJANGO_SETTINGS_MODULE`` environment variable to the module
import path as usual, e.g. in bash::

    export DJANGO_SETTINGS_MODULE=mysite.settings

To enable Django to use your configuration you now have to modify your
``manage.py`` or ``wsgi.py`` script to use django-configurations's versions
of the appropriate starter functions, e.g. a typical ``manage.py`` using
django-configurations would look like this::

    #!/usr/bin/env python
    import os
    import sys
   
    if __name__ == "__main__":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
        os.environ.setdefault('DJANGO_', 'MySettings')
   
        from configurations.management import execute_from_command_line
   
        execute_from_command_line(sys.argv)

Notice in line 9 we don't use the common tool
``django.core.management.execute_from_command_line`` but instead
``configurations.management.execute_from_command_line``.

The same applies to your ``wsgi.py`` file, e.g.::

    import os
  
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'MySettings')
    
    from configurations.wsgi import get_wsgi_application

    application = get_wsgi_application()

Here we don't use the default ``django.core.wsgi.get_wsgi_application``
function but instead ``configurations.wsgi.get_wsgi_application``.

That's it! You can now use your project with ``manage.py`` and your favorite
WSGI enabled server.
