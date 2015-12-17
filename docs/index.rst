.. include:: ../README.rst

Project templates
^^^^^^^^^^^^^^^^^

Don't miss the Django :ref:`project templates pre-configured with
django-configurations<project-templates>` to simplify getting started
with new Django projects.

Wait, what?
-----------

django-configurations helps you organize the configuration of your Django
project by providing the glue code to bridge between Django's module based
settings system and programming patterns like mixins_, facades_, factories_
and adapters_ that are useful for non-trivial configuration scenarios.

It allows you to use the native abilities of Python inheritance without the
side effects of module level namespaces that often lead to the unfortunate
use of the ``from foo import *`` anti-pattern.

.. _mixins: http://en.wikipedia.org/wiki/Mixin
.. _facades: http://en.wikipedia.org/wiki/Facade_pattern
.. _factories: http://en.wikipedia.org/wiki/Factory_method_pattern
.. _adapters: http://en.wikipedia.org/wiki/Adapter_pattern

Okay, how does it work?
-----------------------

Any subclass of the ``configurations.Configuration`` class will automatically
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

.. versionadded:: 0.2

Alternatively you can use the ``--configuration`` command line option that
django-configurations adds to all Django management commands. Behind the
scenes it will simply set the ``DJANGO_CONFIGURATION`` environement variable
so this is purely optional and just there to compliment the default
``--settings`` option that Django adds if you prefer that instead of setting
environment variables.

But isn't that magic?
---------------------

Yes, it looks like magic, but it's also maintainable and non-intrusive.
No monkey patching is needed to teach Django how to load settings via
django-configurations because it uses Python import hooks (`PEP 302`_)
behind the scenes.

.. _`PEP 302`: http://www.python.org/dev/peps/pep-0302/

Further documentation
---------------------

.. toctree::
   :maxdepth: 3

   patterns
   values
   cookbook
   changes

Alternatives
------------

Many thanks to those project that have previously solved these problems:

- The Pinax_ project for spearheading the efforts to extend the Django
  project metaphor with reusable project templates and a flexible
  configuration environment.

- `django-classbasedsettings`_ by Matthew Tretter for being the immediate
  inspiration for django-configurations.

.. _Pinax: http://pinaxproject.com
.. _`django-classbasedsettings`: https://github.com/matthewwithanm/django-classbasedsettings


Bugs and feature requests
-------------------------

As always your mileage may vary, so please don't hesitate to send feature
requests and bug reports:

    https://github.com/jazzband/django-configurations/issues

Thanks!