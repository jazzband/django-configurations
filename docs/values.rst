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

.. note::

  These classes are required to be used as attributes of ``Configuration``
  classes. See the :doc:`main documentation<index>` for more information.

Overview
--------

Here is an example (from a **settings.py** file with a ``Configuration``
subclass):

.. code-block:: python
   :emphasize-lines: 4

    from configurations import Configuration, values

    class Dev(Configuration):
        DEBUG = values.BooleanValue(True)

As you can see all you have to do is to wrap your settings value in a call
to one of the included values classes. When Django's process starts up
it will automatically make sure the passed-in value validates correctly --
in the above case checks if the value is really a boolean.

You can safely use other :class:`~Value` instances as the default setting
value:

.. code-block:: python
   :emphasize-lines: 5

    from configurations import Configuration, values

    class Dev(Configuration):
        DEBUG = values.BooleanValue(True)
        DEBUG_PROPAGATE_EXCEPTIONS = values.BooleanValue(DEBUG)

See the list of :ref:`built-in value classes<built-ins>` for more information.

Environment variables
---------------------

To separate the site configuration from your application code you should use
environment variables for configuration. Unfortunately environment variables
are string based so they are not easily mapped to the Python based settings
system Django uses.

Luckily django-configurations' :class:`~Value` subclasses have the ability
to handle environment variables for the common use cases.

Default behavior
^^^^^^^^^^^^^^^^

For example, imagine you want to override the ``ROOT_URLCONF`` setting on your
staging server to be able to debug a problem with your in-development code.
You're using a web server that passes the environment variables from
the shell it was started from into your Django WSGI process.

Use the boolean ``environ`` option of the :class:`~Value` class (``True`` by
default) to tell django-configurations to look for an environment variable with
the same name as the specific :class:`~Value` variable, only uppercased and
prefixed with ``DJANGO_``. E.g.:

.. code-block:: python
   :emphasize-lines: 5

    from configurations import Configuration, values

    class Stage(Configuration):
        # ..
        ROOT_URLCONF = values.Value('mysite.urls')

django-configurations will try to read the ``DJANGO_ROOT_URLCONF`` environment
variable when deciding which value the ``ROOT_URLCONF`` setting should have.
When you run the web server simply specify that environment variable
(e.g. in your init script)::

    DJANGO_ROOT_URLCONF=mysite.debugging_urls gunicorn mysite.wsgi:application

If the environment variable can't be found it'll use the default
``'mysite.urls'``.

Disabling environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To disable environment variables, specify the ``environ`` parameter of the
:class:`~Value` class. For example this would disable it for the ``TIME_ZONE``
setting value::

    from configurations import Configuration, values

    class Dev(Configuration):
        TIME_ZONE = values.Value('UTC', environ=False)

Custom environment variable names
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To support legacy systems, integrate with other parts of your software stack or
simply better match your taste in naming public configuration variables,
django-configurations allows you to use the ``environ_name`` parameter of the
:class:`~Value` class to change the base name of the environment variable it
looks for. For example this would enforce the name ``DJANGO_MYSITE_TZ``
instead of using the name of the :class:`~Value` instance.::

    from configurations import Configuration, values

    class Dev(Configuration):
        TIME_ZONE = values.Value('UTC', environ_name='MYSITE_TZ')

Allow final value to be used outside the configuration context
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may use the ``environ_name`` parameter to allow a :class:`~Value` to be
directly converted to its final value for use outside of the configuration
context::

    >>> type(values.Value([]))
    <class 'configurations.values.Value'>
    >>> type(values.Value([], environ_name="FOOBAR"))
    <class 'list'>

This can also be achieved when using ``environ=False`` and providing a
default value.

Custom environment variable prefixes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In case you want to change the default environment variable name prefix
of ``DJANGO`` to something to your likening, use the ``environ_prefix``
parameter of the :class:`~Value` instance. Here it'll look for the
``MYSITE_TIME_ZONE`` environment variable (instead of ``DJANGO_TIME_ZONE``)::

    from configurations import Configuration, values

    class Dev(Configuration):
        TIME_ZONE = values.Value('UTC', environ_prefix='MYSITE')

The ``environ_prefix`` parameter can also be ``None`` to completely disable
the prefix.

``Value`` class
---------------

.. class:: Value(default, [environ=True, environ_name=None, environ_prefix='DJANGO', environ_required=False])

   The ``Value`` class takes one required and several optional parameters.

   :param default: the default value of the setting
   :param environ: toggle for environment use
   :param environ_name: capitalized name of environment variable to look for
   :param environ_prefix: capitalized prefix to use when looking for environment variable
   :param environ_required: whether or not the value is required to be set as an environment variable
   :type environ: bool
   :type environ_name: str or None
   :type environ_prefix: str
   :type environ_required: bool

   The ``default`` parameter is effectively the value the setting has
   right now in your ``settings.py``.

   .. method:: setup(name)

      :param name: the name of the setting
      :return: setting value

      The ``setup`` method is called during startup of the Django process and
      implements the ability to check the environment variable. Its purpose is
      to return a value django-configurations is supposed to use when loading
      the settings. It'll be passed one parameter, the name of the
      :class:`~Value` instance as defined in the ``settings.py``. This is used
      for building the name of the environment variable.

   .. method:: to_python(value)

      :param value: the value of the setting as found in the process
                    environment (:data:`os.environ`)
      :return: validated and "ready" setting value if found in process
               environment

      The ``to_python`` method is used when the ``environ`` parameter of the
      :class:`~Value` class is set to ``True`` (the default) and an
      environment variable with the appropriate name was found.

      It will be used to handle the string based environment variables and
      returns the "ready" value of the setting.

      Some :class:`~Value` subclasses also use it during initialization when the
      default value has a string-like format like an environment variable which
      needs to be converted into a Python data type.

.. _built-ins:

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

        MYSITE_CACHE_TIMEOUT = values.IntegerValue(3600)

.. class:: PositiveIntegerValue

    A :class:`~Value` subclass that handles positive integer values.

    .. versionadded:: 2.1

    ::

        MYSITE_WORKER_POOL = values.PositiveIntegerValue(8)

.. class:: FloatValue

    A :class:`~Value` subclass that handles float values.

    ::

        MYSITE_TAX_RATE = values.FloatValue(11.9)

.. class:: DecimalValue

    A :class:`~Value` subclass that handles Decimal values.

    ::

        MYSITE_CONVERSION_RATE = values.DecimalValue(decimal.Decimal('4.56214'))

.. class:: SequenceValue

   Common base class for sequence values.

.. class:: ListValue(default, [separator=',', converter=None])

    A :class:`~SequenceValue` subclass that handles list values.

    :param separator: the separator to split environment variables with
    :param converter: the optional converter callable to apply for each list
                      item

    Simple example::

        ALLOWED_HOSTS = ListValue(['mysite.com', 'mysite.biz'])

    Use a custom converter to check for the given variables::

        def check_monty_python(person):
            if not is_completely_different(person):
                error = '{0} is not a Monty Python member'.format(person)
                raise ValueError(error)
            return person

        MONTY_PYTHONS = ListValue(['John Cleese', 'Eric Idle'],
                                  converter=check_monty_python)

    You can override this list with an environment variable like this::

        DJANGO_MONTY_PYTHONS="Terry Jones,Graham Chapman" gunicorn mysite.wsgi:application

    Use a custom separator::

        EMERGENCY_EMAILS = ListValue(['admin@mysite.net'], separator=';')

    And override it::

        DJANGO_EMERGENCY_EMAILS="admin@mysite.net;manager@mysite.org;support@mysite.com" gunicorn mysite.wsgi:application

.. class:: TupleValue

    A :class:`~SequenceValue` subclass that handles tuple values.

    :param separator: the separator to split environment variables with
    :param converter: the optional converter callable to apply for each tuple
                      item

    See the :class:`~ListValue` examples above.

.. class:: SingleNestedSequenceValue

   Common base class for nested sequence values.

.. class:: SingleNestedTupleValue(default, [seq_separator=';', separator=',', converter=None])

    A :class:`~SingleNestedSequenceValue` subclass that handles single nested tuple values,
    e.g. ``((a, b), (c, d))``.

    :param seq_separator: the separator to split each tuple with
    :param separator: the separator to split the inner tuple contents with
    :param converter: the optional converter callable to apply for each inner
                      tuple item

    Useful for ADMINS, MANAGERS, and the like.  For example::

        ADMINS = SingleNestedTupleValue((
            ('John', 'jcleese@site.com'),
            ('Eric', 'eidle@site.com'),
        ))

    Override using environment variables like this::

        DJANGO_ADMINS=Terry,tjones@site.com;Graham,gchapman@site.com

.. class:: SingleNestedListValue(default, [seq_separator=';', separator=',', converter=None])

    A :class:`~SingleNestedSequenceValue` subclass that handles single nested list values,
    e.g. ``[[a, b], [c, d]]``.

    :param seq_separator: the separator to split each list with
    :param separator: the separator to split the inner list contents with
    :param converter: the optional converter callable to apply for each inner
                      list item

    See the :class:`~SingleNestedTupleValue` examples above.

.. class:: SetValue

    A :class:`~Value` subclass that handles set values.

    :param separator: the separator to split environment variables with
    :param converter: the optional converter callable to apply for each set
                      item

    See the :class:`~ListValue` examples above.

.. class:: DictValue

    A :class:`~Value` subclass that handles dicts.

     ::

        DEPARTMENTS = values.DictValue({
            'it': ['Mike', 'Joe'],
        })

    Override using environment variables like this::

        DJANGO_DEPARTMENTS={'it':['Mike','Joe'],'hr':['Emma','Olivia']}

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

.. class:: RegexValue(default, regex, [environ=True, environ_name=None, environ_prefix='DJANGO'])

    A :class:`~Value` subclass that validates according a regular expression
    and uses the :class:`django:django.core.validators.RegexValidator`.

    :param regex: the regular expression

    ::

        DEFAULT_SKU = values.RegexValue('000-000-00', regex=r'\d{3}-\d{3}-\d{2}')

.. class:: PathValue(default, [check_exists=True, environ=True, environ_name=None, environ_prefix='DJANGO'])

    A :class:`~Value` subclass that normalizes the given path using
    :func:`os.path.expanduser` and checks if it exists on the file system.

    Takes an optional ``check_exists`` parameter to disable the check with
    :func:`os.path.exists`.

    :param check_exists: toggle the file system check

    ::

        BASE_DIR = values.PathValue('/opt/mysite/')
        STATIC_ROOT = values.PathValue('/var/www/static', checks_exists=False)

URL-based values
^^^^^^^^^^^^^^^^

.. note::

  The following URL-based :class:`~Value` subclasses are inspired by the
  `Twelve-Factor methodology`_ and use environment variable names that are
  already established by that methodology, e.g. ``'DATABASE_URL'``.

  Each of these classes require external libraries to be installed, e.g. the
  :class:`~DatabaseURLValue` class depends on the package ``dj-database-url``.
  See the specific class documentation below for which package is needed.

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
      different settings variables. `dj-email-url`_ supports all options
      though and simply returns a nested dictionary of settings instead of
      just one setting.

    The parameters have the following default values:

    :param environ: ``True``
    :param environ_name: ``EMAIL_URL``
    :param environ_prefix: ``None``

    ::

        EMAIL = values.EmailURLValue('console://')

    .. _`dj-email-url`: https://pypi.python.org/pypi/dj-email-url/

.. class:: SearchURLValue(default, [environ=True, environ_name='SEARCH_URL', environ_prefix=None])

    .. versionadded:: 0.8

    A :class:`~Value` subclass that uses the `dj-search-url`_ app to
    convert a search configuration value stored in the ``SEARCH_URL``
    environment variable into the appropriate settings for use with Haystack_.
    It's inspired by the `Twelve-Factor methodology`_.

    By default this :class:`~Value` subclass looks for the ``SEARCH_URL``
    environment variable.

    Takes an optional ``alias`` parameter to define which search backend alias
    to use for the ``HAYSTACK_CONNECTIONS`` setting.

    :param alias: which cache alias to use

    The other parameters have the following default values:

    :param environ: ``True``
    :param environ_name: ``SEARCH_URL``
    :param environ_prefix: ``None``

    ::

        HAYSTACK_CONNECTIONS = values.SearchURLValue('elasticsearch://127.0.0.1:9200/my-index')

    .. _`dj-search-url`: https://pypi.python.org/pypi/dj-search-url/
    .. _Haystack: http://haystacksearch.org/

Other values
^^^^^^^^^^^^

.. class:: BackendsValue

    A :class:`~ListValue` subclass that validates the given list of dotted
    import paths by trying to import them. In other words, this checks if
    the backends exist.

    ::

        MIDDLEWARE = values.BackendsValue([
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
    file. This usually resolves to ``DJANGO_SECRET_KEY`` unless you have
    customized the environment variable names.

    :raises: ``ValueError`` when given a default value

    .. versionchanged:: 1.0

      This value class has the ``environ_required`` parameter turned to
      ``True``.

    ::

        SECRET_KEY = values.SecretValue()

Value mixins
^^^^^^^^^^^^

.. class:: CastingMixin

    A mixin to be used with one of the :class:`~Value` subclasses that
    requires a ``caster`` class attribute of one of the following types:

    - dotted import path, e.g. ``'mysite.utils.custom_caster'``
    - a callable, e.g. :class:`int`

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
    - a callable, e.g. :class:`bool`

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
