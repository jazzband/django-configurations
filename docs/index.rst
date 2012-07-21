.. include:: ../README.rst

Wait, what?
-----------

django-configurations helps you organize the configuration of your Django
project by providing the glue code to bridge between Django's module based
settings system and programming patterns like mixins_, facades_, factories_
and adapters_ that are useful for non-trivial configuration scenarios.

It allows you to use the native abilities of Python inheritance without the
side effects of module level namespaces that often lead to the unfortunate
use of the ``import *`` anti-pattern.

.. _mixins: http://en.wikipedia.org/wiki/Mixin
.. _facades: http://en.wikipedia.org/wiki/Facade_pattern
.. _factories: http://en.wikipedia.org/wiki/Factory_method_pattern
.. _adapters: http://en.wikipedia.org/wiki/Adapter_pattern

Okay, how does it work?
-----------------------

Any subclass of the ``configurations.Settings`` class will automatically
use the values of its class and instance attributes (including properties
and methods) to set module level variables of the same module -- that's
how Django will interface to the django-configurations based settings during
startup and also the reason why it requires you to use its own startup
functions.

That means when Django starts up django-configurations will have a look at
the ``DJANGO_CONFIGURATION`` environment variable to figure out which class
in the settings module (as defined by the ``DJANGO_SETTINGS_MODULE``
environment variable) should be used for the process. It then instantiates
the class defined with ``DJANGO_CONFIGURATION`` and copies the uppercase
attributes to the module level variables.

But isn't that magic?
---------------------

Yes, it looks like magic, but it's also maintainable and non-intrusive.
No monkey patching is needed to teach Django how to load settings via
django-configurations because it uses Python import hooks (`PEP 302`_)
behind the scenes.

.. _`PEP 302`: http://www.python.org/dev/peps/pep-0302/

Usage patterns
--------------

There are various configuration patterns that can be implemented with
django-configurations. The most common pattern is to have a base class
and various subclasses based on the enviroment they are supposed to be
used in, e.g. in production, staging and development.

Server specific settings
^^^^^^^^^^^^^^^^^^^^^^^^

For example, imagine you have a base setting class in your ``settings.py``
file::

    from configurations import Settings

    class Base(Settings):
        TIME_ZONE = 'Europe/Berlin'

    class Dev(Base):
        DEBUG = True
        TEMPLATE_DEBUG = DEBUG

    class Prod(Base):
        TIME_ZONE = 'America/New_York'

You can now set the ``DJANGO_CONFIGURATION`` environment variable to one
of the class names you've defined, e.g. on your production server it
should be ``Prod``. In bash that would be::

    export DJANGO_SETTINGS_MODULE=mysite.settings
    export DJANGO_CONFIGURATION=Prod

Global settings defaults
^^^^^^^^^^^^^^^^^^^^^^^^

Every ``configurations.Settings`` subclass will automatically contain
Django's global settings as class attributes, so you can refer to them when
setting other values, e.g.::

    from configurations import Settings

    class Base(Settings):
        TEMPLATE_CONTEXT_PROCESSORS = \
            Settings.TEMPLATE_CONTEXT_PROCESSORS + (
                'django.core.context_processors.request',
            )

        @property
        def LANGUAGES(self):
            return Settings.LANGUAGES + (('tlh', 'Klingon'),)

Mixins
^^^^^^

You might want to apply some configuration values for each and every
project you're working on without having to repeat yourself. Just define
a few mixin you re-use multiple times::

    class FullPageCaching(object):
        USE_ETAGS = True

Then import that mixin class in your site settings module and use it with
a Settings class::

    from configurations import Settings

    class AcmeProd(Settings, FullPageCaching):
        DEBUG = False
        # ...

Thanks
------

- The Pinax_ project for spearheading the efforts to extend the Django
  project metaphor with reusable project templates and a flexible
  configuration environment.

- `django-classbasedsettings`_ by Matthew Tretter for being the immediate
  inspiration for django-configurations.

.. _Pinax: http://pinaxproject.com
.. _`django-classbasedsettings`: https://github.com/matthewwithanm/django-classbasedsettings

Bugs and feature requests
-------------------------

As always you mileage may vary, so please don't hesitate to send in feature
requests and bug reports at the usual place:

    https://github.com/jezdez/django-configurations/issues

Thanks!