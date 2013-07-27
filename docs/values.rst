Values
======

.. module:: configurations.values
   :synopsis: Optional value classes for high-level validation and behavior.

.. versionadded:: 0.4

  django-configurations allows you to optionally reduce the amount of validation
  and setup code in your **settings.py** by using ``Value`` classes. They have
  the ability to handle values from the process environment of your software
  (:data:`os.environ`) and work well in projects that follow the
  `Twelve-Factor methodology`_.

Overview
--------

Here is an example (from a **settings.py**)::

    from configurations import values

    DEBUG = values.BooleanValue(True)

As you can see all you have to do is to wrap your settings value in a call
to one of the included settings classes. When Django's process starts up
it will automatically make sure the passed in value validates correctly --
in the above case checks if the value is really a boolean.

You can safely use other :class:`~Value` instances as the default setting
value::

    from configurations import values

    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = values.BooleanValue(DEBUG)

See the list of built-in value classes for more information.

Environment variables
---------------------

To separate configuration from your application you should use environment
variables to override settings values if needed. Unfortunately environment
variables are string based so they are not easily mapped to the Python based
settings system Django uses.

Luckily django-configurations' :class:`~Value` subclasses have the ability
to handle environment variables for the most common use cases.

For example, imagine you'd like to override the ``TEMPLATE_DEBUG`` setting
on your staging server to be able to debug a problem with your in-development
code. You're using a web server that passes the environment variables from
the shell it was started in to your Django WSGI process.

First make sure you set the ``environ`` option of the :class:`~Value` instance
to ``True``::

    from configurations import values

    # ..
    TEMPLATE_DEBUG = values.BooleanValue(True, environ=True)

That will tell django-configurations to look for a environment variable
named ``DJANGO_TEMPLATE_DEBUG`` when deciding which value of the ``DEBUG``
setting to actually enable.

When you run your web server simply specify that environment variable
(e.g. in your init script)::

    DJANGO_TEMPLATE_DEBUG=true gunicorn mysite.wsgi:application

Since environment variables are string based the ``BooleanValue`` supports
a series of possible formats for a boolean value (``true``, ``yes``,
``y`` and ``1``, all in capital and lower case, and ``false``, ``no``,
``n`` and ``0`` of course). So for example this will work, too::

    DJANGO_TEMPLATE_DEBUG=no ./manage.py runserver

``Value`` class
---------------

.. class:: Value(default, [environ=False, environ_name=None, environ_prefix='DJANGO'])
    
   The ``Value`` class takes one required and several optional parameters.

   :param default: the default value of the setting
   :param environ: toggle for environment use
   :param environ_name: name of environment variable to look for
   :param environ_prefix: prefix to use when looking for environment variable
   :type environ: bool
   :type environ_name: capitalized string or None
   :type environ_prefix: capitalized string

   The ``default`` parameter is effectively the value the setting has
   right now in your ``settings.py``.
 
   .. method:: setup(name)

      :param name: the name of the setting
      :return: setting value

      The ``setup`` method is called during startup of the Django process and
      implements the ability to check the environment variable. Its purpose is
      to return a value django-configrations is supposed to use when loading
      the settings. It'll be passed one parameter, the name of the
      :class:`~Value` instance as defined in the ``settings.py``. This is used
      for building the name of the environment variable.
 
   .. method:: to_python(value)

      :param value: the value of the setting as found in the process
                    environment (:data:`os.environ`)
      :return: validated and "ready" setting value if found in process
               environment      

      The ``to_python`` method is only used when the ``environ`` parameter
      of the :class:`~Value` class is set to ``True`` and an environment
      variable with the appropriate name was found. It will be used to handle
      the string based environment variable values and returns the "ready"
      value to be returned by the ``setup`` method.

Built-ins
---------

Type values
^^^^^^^^^^^

.. class:: BooleanValue

    A :class:`~Value` subclass that checks and returns boolean values. Possible
    values for environment variables are:

    - ``True`` values: ``'yes'``, ``'y'``, ``'true'``, ``'1'``
    - ``False`` values: ``'no'``, ``'n'``, ``'false'``, ``'0'``,
      ``''`` (empty string)

    ::

        DEBUG = values.BooleanValue(True)

.. class:: IntegerValue

    A :class:`~Value` subclass that handles integer values.

    ::

        MYSITE_CACHE_TIMEOUT = values.BooleanValue(3600)

.. class:: FloatValue

    A :class:`~Value` subclass that handles float values.

    ::

        MYSITE_TAX_RATE = values.FloatValue(11.9)

.. class:: DecimalValue

    A :class:`~Value` subclass that handles Decimal values.

    ::

        MYSITE_CONVERSION_RATE = values.DecimalValue(decimal.Decimal('4.56214'))

.. class:: ListValue(default, [separator=',', converter=None])

    A :class:`~Value` subclass that handles list values.

    :param separator: the separator to split environment variables with
    :param converter: the optional converter callable to apply for each list
                      item

    Simple example::

        ALLOWED_HOSTS = ListValue(['mysite.com', 'mysite.biz'])

    Use a custom converter to check for the given variables::

        def check_monty_python(person):
            if not is_completely_different(person):
                raise ValueError('{0} is not a Monty Python member'.format(person))
            return person

        MONTY_PYTHONS = ListValue(['John Cleese', 'Eric Idle'],
                                  converter=check_monty_python,
                                  environ=True)

    You can override this list with an environment variable like this::

        DJANGO_MONTY_PYTHONS="Terry Jones,Graham Chapman" gunicorn mysite.wsgi:application

    Use a custom separator::

        EMERGENCY_EMAILS = ListValue(['admin@mysite.net'],
                                     separator=';', environ=True)

    And override it::

        DJANGO_EMERGENCY_EMAILS="admin@mysite.net;manager@mysite.org;support@mysite.com" gunicorn mysite.wsgi:application

.. class:: TupleValue

    A :class:`~Value` subclass that handles tuple values.

    :param separator: the separator to split environment variables with
    :param converter: the optional converter callable to apply for each tuple
                      item

    See the :class:`~ListValue` examples above.

.. class:: SetValue

    A :class:`~Value` subclass that handles set values.

    :param separator: the separator to split environment variables with
    :param converter: the optional converter callable to apply for each set
                      item

    See the :class:`~ListValue` examples above.

.. class:: DictValue

Validator values
^^^^^^^^^^^^^^^^

.. class:: EmailValue

    A :class:`~Value` subclass that validates the value using the
    :data:`django:django.core.validators.validate_email` validator.

    ::

        SUPPORT_EMAIL = values.EmailValue('support@mysite.com')

.. class:: URLValue

    A :class:`~Value` subclass that validates the value using the
    :class:`django:django.core.validators.URLValidator` validator.

    ::

        SUPPORT_URL = values.URLValue('https://support.mysite.com/')

.. class:: IPValue

    A :class:`~Value` subclass that validates the value using the
    :data:`django:django.core.validators.validate_ipv46_address` validator.

    ::

        LOADBALANCER_IP = values.IPValue('127.0.0.1')

.. class:: RegexValue(default, regex, [environ=False, environ_name=None, environ_prefix='DJANGO'])

    A :class:`~Value` subclass that validates according a regular expression
    and uses the :class:`django:django.core.validators.RegexValidator`.

    :param regex: the regular expression

    ::

        DEFAULT_SKU = values.RegexValue('000-000-00', regex=r'\d{3}-\d{3}-\d{2}')

.. class:: PathValue(default, [check_exists=True, environ=False, environ_name=None, environ_prefix='DJANGO'])

    A :class:`~Value` subclass that normalizes the given path using
    :func:`os.path.expanduser` and validates if it exists on the file system.

    Takes an optional ``check_exists`` parameter to disable the check with
    :func:`os.path.exists`.

    :param check_exists: toggle the file system check

    ::

        BASE_DIR = values.PathValue('/opt/mysite/')

URL-based values
^^^^^^^^^^^^^^^^

.. note::

  The following URL-based :class:`~Value` subclasses behave slightly different
  to the rest of the classes here. They are inspired by the
  `Twelve-Factor methodology`_ and by default inspect the :data:`os.environ`
  using a previously established environment variable name, e.g.
  ``DATABASE_URL``.

  Each of them require having an external library installed, e.g. the
  :class:`~DatabaseURLValue` class depends on the package ``dj-database-url``.

.. class:: DatabaseURLValue(default, [alias='default', environ=True, environ_name='DATABASE_URL', environ_prefix=None])

    A :class:`~Value` subclass that uses the `dj-database-url`_ app to
    convert a database configuration value stored in the ``DATABASE_URL``
    environment variable into an appropriate setting value. It's inspired by
    the `Twelve-Factor methodology`_.

    By default this :class:`~Value` subclass looks for the ``DATABASE_URL``
    environment variable.

    Takes an optional ``alias`` parameter to define which database alias to
    use for the ``DATABASES`` setting.

    :param alias: which database alias to use

    The other parameters have the following default values:

    :param environ: ``True``
    :param environ_name: ``DATABASE_URL``
    :param environ_prefix: ``None``

    ::

        DATABASES = values.DatabaseURLValue('postgres://myuser@localhost/mydb')

    .. _`dj-database-url`: https://pypi.python.org/pypi/dj-database-url/

.. class:: CacheURLValue(default, [alias='default', environ=True, environ_name='CACHE_URL', environ_prefix=None])

    A :class:`~Value` subclass that uses the `django-cache-url`_ app to
    convert a cache configuration value stored in the ``CACHE_URL``
    environment variable into an appropriate setting value. It's inspired by
    the `Twelve-Factor methodology`_.

    By default this :class:`~Value` subclass looks for the ``CACHE_URL``
    environment variable.

    Takes an optional ``alias`` parameter to define which database alias to
    use for the ``CACHES`` setting.

    :param alias: which cache alias to use

    The other parameters have the following default values:

    :param environ: ``True``
    :param environ_name: ``CACHE_URL``
    :param environ_prefix: ``None``

    ::

        CACHES = values.CacheURLValue('memcached://127.0.0.1:11211/')

    .. _`django-cache-url`: https://pypi.python.org/pypi/django-cache-url/

.. class:: EmailURLValue(default, [environ=True, environ_name='EMAIL_URL', environ_prefix=None])

    A :class:`~Value` subclass that uses the `dj-email-url`_ app to
    convert an email configuration value stored in the ``EMAIL_URL``
    environment variable into the appropriate settings. It's inspired by
    the `Twelve-Factor methodology`_.

    By default this :class:`~Value` subclass looks for the ``EMAIL_URL``
    environment variable.

    .. note::

      This is a special value since email settings are divided into many
      different settings. `dj-email-url`_ supports all options though and
      simply returns a nested dictionary of settings instead of just one
      setting.

    The parameters have the following default values:

    :param environ: ``True``
    :param environ_name: ``EMAIL_URL``
    :param environ_prefix: ``None``

    ::

        EMAIL_URL = values.EmailURLValue('console://')

    .. _`dj-email-url`: https://pypi.python.org/pypi/dj-email-url/

Other values
^^^^^^^^^^^^

.. class:: BackendsValue

    A :class:`~ListValue` subclass that validates the given list of dotted
    import paths by trying to import them. In other words, this checks if
    the backends exist.

    ::

        MIDDLEWARE_CLASSES = values.BackendsValue([
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ])

.. class:: SecretValue

    A :class:`~Value` subclass that doesn't allow setting a default value
    during instantiation and force-enables the use of an environment variable
    to reduce the risk of accidentally storing secret values in the settings
    file.

    :raises: ``ValueError`` when given a default value

    ::

        SECRET_KEY = values.SecretValue()

Value mixins
^^^^^^^^^^^^

.. class:: CastingMixin

    A mixin to be used with one of the :class:`~Value` subclasses that
    requires a ``caster`` class attribute of one of the following types:

    - dotted import path, e.g. ``'mysite.utils.custom_caster'``
    - a callable, e.g. :func:`int`

    Example::

        class TemparatureValue(CastingMixin, Value):
            caster = 'mysite.temperature.fahrenheit_to_celcius'

    Optionally it can take a ``message`` class attribute as the error
    message to be shown if the casting fails. Additionally an ``exception``
    parameter can be set to a single or a tuple of exception classes that
    are required to be handled during the casting.

.. class:: ValidationMixin

    A mixin to be used with one of the :class:`~Value` subclasses that
    requires a ``validator`` class attribute of one of the following types:
    The validator should raise Django's
    :exc:`~django.core.exceptions.ValidationError` to indicate a failed
    validation attempt.

    - dotted import path, e.g. ``'mysite.validators.custom_validator'``
    - a callable, e.g. :func:`bool`

    Example::

        class TemparatureValue(ValidationMixin, Value):
            validator = 'mysite.temperature.is_valid_temparature'

    Optionally it can take a ``message`` class attribute as the error
    message to be shown if the validation fails.

.. class:: MultipleMixin

    A mixin to be used with one of the :class:`~Value` subclasses that
    enables the return value of the :func:`~Value.to_python` to be
    interpreted as a dictionary of settings values to be set at once,
    instead of using the return value to just set one setting.

    A good example for this mixin is the :class:`~EmailURLValue` value
    which requires setting many ``EMAIL_*`` settings.

.. _`Twelve-Factor methodology`: http://www.12factor.net/
