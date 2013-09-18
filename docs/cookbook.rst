Cookbook
========

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

.. _project-templates:

Project templates
-----------------

You can use a special Django project template that is a copy of the one
included in Django 1.5.x and 1.6.x. The following examples assumes you're
using pip_ to install packages.

Django 1.5.x
^^^^^^^^^^^^

First install Django 1.5.x and django-configurations::

    pip install -r https://raw.github.com/jezdez/django-configurations/templates/1.5.x/requirements.txt

Then create your new Django project with the provided template::

    django-admin.py startproject mysite -v2 --template https://github.com/jezdez/django-configurations/archive/templates/1.5.x.zip

See the repository of the template for more information:

    https://github.com/jezdez/django-configurations/tree/templates/1.5.x

Django 1.6.x
^^^^^^^^^^^^

First install Django 1.6.x and django-configurations::

    pip install -r https://raw.github.com/jezdez/django-configurations/templates/1.6.x/requirements.txt

Or Django 1.6::

    django-admin.py startproject mysite -v2 --template https://github.com/jezdez/django-configurations/archive/templates/1.6.x.zip

Now you have a default Django 1.5.x or 1.6.x project in the ``mysite``
directory that uses django-configurations.

See the repository of the template for more information:

    https://github.com/jezdez/django-configurations/tree/templates/1.6.x

.. _pip: http://pip-installer.org/

Celery
------

Given Celery's way to load Django settings in worker processes you should
probably just add the following to the **beginning** of your settings module::

    from configurations import importer
    importer.install()

That has the same effect as using the ``manage.py`` or ``wsgi.py`` utilities.

iPython notebooks
-----------------

.. versionadded:: 0.6

To use django-configurations with IPython_'s great notebooks, you have to
enable an extension in your IPython configuration. See the IPython
documentation for how to create and `manage your IPython profile`_ correctly.

Here's a quick how-to in case you don't have a profile yet. Type in your
command line shell::

    ipython profile create

Then let IPython show you where the configuration file ``ipython_config.py``
was created::

    ipython locate profile

That should print a directory path where you can find the
``ipython_config.py`` configuration file. Now open that file and extend the
``c.InteractiveShellApp.extensions`` configuration value. It may be commented
out from when IPython created the file or it may not exist in the file at all.
In either case make sure it's not a Python comment anymore and reads like this::

    # A list of dotted module names of IPython extensions to load.
    c.InteractiveShellApp.extensions = [
        # .. your other extensions if available
        'configurations',
    ]

That will tell IPython to load django-configurations correctly on startup.
It also works with django-extensions's shell_plus_ management command.

.. _IPython: http://ipython.org/
.. _`manage your IPython profile`: http://ipython.org/ipython-doc/dev/config/overview.html#configuration-file-location
.. _shell_plus: http://django-extensions.readthedocs.org/en/latest/shell_plus.html

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
