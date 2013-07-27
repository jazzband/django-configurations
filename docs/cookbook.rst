Cookbook
========

Celery
------

Given Celery's way to load Django settings in worker processes you should
probably just add the following to the **begin** of your settings module::

    from configurations import importer
    importer.install()

That has the same effect as using the ``manage.py`` or ``wsgi.py`` utilities
mentioned above.

FastCGI
-------

In case you use FastCGI for deploying Django (you really shouldn't) and aren't
allowed to us Django's runfcgi_ management command (that would automatically
handle the setup for your if you've followed the quickstart guide above), make
sure to use something like the following script::

    #!/usr/bin/env python

    import os
    import sys
     
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'MySiteConfiguration')

    from configurations.fastcgi import runfastcgi

    runfastcgi(method='threaded', daemonize='true')

As you can see django-configurations provides a helper module
``configurations.fastcgi`` that handles the setup of your configurations.

.. _runfcgi: https://docs.djangoproject.com/en/1.5/howto/deployment/fastcgi/

Envdir
------

envdir_ is an effective way to set a large number of environment variables
at once during startup of a command. This is great in combination with
django-configuration's :class:`~configurations.values.Value` subclasses
when enabling their ability to check environment variables for override
values.

Imagine for example you want to set a few environment variables, all you
have to do is to create a directory with files that have capitalized names
and contain the values you want to set.

Example::

    $ tree mysite_env/
    mysite_env/
    ├── DJANGO_SETTINGS_MODULE
    ├── DJANGO_DEBUG
    ├── DJANGO_DATABASE_URL
    ├── DJANGO_CACHE_URL
    └── PYTHONSTARTUP

    0 directories, 3 files
    $ cat mysite_env/DJANGO_CACHE_URL
    redis://user@host:port/1
    $

Then, to enable the ``mysite_env`` environment variables, simply use the
``envdir`` command line tool as a prefix for your program, e.g.::

    $ envdir mysite_env python manage.py runserver

See envdir_ documentation for more information, e.g. using envdir_ from
Python instead of from the command line.

.. _envdir: https://pypi.python.org/pypi/envdir
