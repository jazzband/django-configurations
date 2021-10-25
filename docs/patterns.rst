Usage patterns
==============

There are various configuration patterns that can be implemented with
django-configurations. The most common pattern is to have a base class
and various subclasses based on the enviroment they are supposed to be
used in, e.g. in production, staging and development.

Server specific settings
------------------------

For example, imagine you have a base setting class in your **settings.py**
file:

.. code-block:: python

    from configurations import Configuration

    class Base(Configuration):
        TIME_ZONE = 'Europe/Berlin'

    class Dev(Base):
        DEBUG = True

    class Prod(Base):
        TIME_ZONE = 'America/New_York'

You can now set the ``DJANGO_CONFIGURATION`` environment variable to
one of the class names you've defined, e.g. on your production server
it should be ``Prod``. In Bash that would be:

.. code-block:: console

    export DJANGO_SETTINGS_MODULE=mysite.settings
    export DJANGO_CONFIGURATION=Prod
    python manage.py runserver

Alternatively you can use the ``--configuration`` option when using Django
management commands along the lines of Django's default ``--settings``
command line option, e.g.

.. code-block:: console

    python manage.py runserver --settings=mysite.settings --configuration=Prod

Property settings
-----------------

Use a ``property`` to allow for computed settings. This pattern can
also be used to postpone / lazy evaluate a value. E.g., useful when
nesting a Value in a dictionary and a string is required:

.. code-block:: python

    class Prod(Configuration):
        SOME_VALUE = values.Value(None, environ_prefix=None)

        @property
        def SOME_CONFIG(self):
            return {
                'some_key': self.SOME_VALUE,
            }

Global settings defaults
------------------------

Every ``configurations.Configuration`` subclass will automatically
contain Django's global settings as class attributes, so you can refer
to them when setting other values, e.g.

.. code-block:: python

    from configurations import Configuration

    class Prod(Configuration):
        TEMPLATE_CONTEXT_PROCESSORS = Configuration.TEMPLATE_CONTEXT_PROCESSORS + (
                'django.core.context_processors.request',
            )

        @property
        def LANGUAGES(self):
            return list(Configuration.LANGUAGES) + [('tlh', 'Klingon')]

Configuration mixins
--------------------

You might want to apply some configuration values for each and every
project you're working on without having to repeat yourself. Just define
a few mixin you re-use multiple times:

.. code-block:: python

    class FullPageCaching:
        USE_ETAGS = True

Then import that mixin class in your site settings module and use it with
a ``Configuration`` class:

.. code-block:: python

    from configurations import Configuration

    class Prod(FullPageCaching, Configuration):
        DEBUG = False
        # ...

Pristine methods
----------------

.. versionadded:: 0.3

In case one of your settings itself need to be a callable, you need to
tell that django-configurations by using the ``pristinemethod``
decorator, e.g.

.. code-block:: python

    from configurations import Configuration, pristinemethod

    class Prod(Configuration):

        @pristinemethod
        def ACCESS_FUNCTION(user):
            return user.is_staff

Lambdas work, too:

.. code-block:: python

    from configurations import Configuration, pristinemethod

    class Prod(Configuration):
        ACCESS_FUNCTION = pristinemethod(lambda user: user.is_staff)


.. _setup-methods:

Setup methods
-------------

.. versionadded:: 0.3

If there is something required to be set up before, during or after the
settings loading happens, please override the ``pre_setup``, ``setup`` or
``post_setup`` class methods like so (don't forget to apply the Python
``@classmethod`` decorator):

.. code-block:: python

    import logging
    from configurations import Configuration

    class Prod(Configuration):
        # ...

        @classmethod
        def pre_setup(cls):
            super(Prod, cls).pre_setup()
            if something.completely.different():
                cls.DEBUG = True

        @classmethod
        def setup(cls):
            super(Prod, cls).setup()
            logging.info('production settings loaded: %s', cls)

        @classmethod
        def post_setup(cls):
            super(Prod, cls).post_setup()
            logging.debug("done setting up! \o/")

As you can see above the ``pre_setup`` method can also be used to
programmatically change a class attribute of the settings class and it
will be taken into account when doing the rest of the settings setup.
Of course that won't work for ``post_setup`` since that's when the
settings setup is already done.

In fact you can easily do something unrelated to settings, like
connecting to a database:

.. code-block:: python

    from configurations import Configuration

    class Prod(Configuration):
        # ...

        @classmethod
        def post_setup(cls):
            import mango
            mango.connect('enterprise')

.. warning::

    You could do the same by overriding the ``__init__`` method of your
    settings class but this may cause hard to debug errors because
    at the time the ``__init__`` method is called (during Django
    startup) the Django setting system isn't fully loaded yet.

    So anything you do in ``__init__`` that may require
    ``django.conf.settings`` or Django models there is a good chance it
    won't work. Use the ``post_setup`` method for that instead.

.. versionchanged:: 0.4

    A new ``setup`` method was added to be able to handle the new
    :class:`~configurations.values.Value` classes and allow an
    in-between modification of the configuration values.

Standalone scripts
------------------

If you want to run scripts outside of your project you need to add
these lines on top of your file:

.. code-block:: python

    import configurations
    configurations.setup()
