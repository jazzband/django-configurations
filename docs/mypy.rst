mypy plugin
===========

Due to Django's dynamic nature, some `mypy plugins`_ such as `django-stubs`_
and `djangorestframework-stubs`_ need to (partially) execute your Django code to
properly derive type information. The django-configurations mypy plugin calls
``configurations.importer.install()`` to initialize your settings on startup so
that plugins like django-stubs and djangorestframework-stubs can work with
projects using django-configurations.

.. _`mypy plugins`: https://mypy.readthedocs.io/en/stable/extending_mypy.html#extending-mypy-using-plugins
.. _`django-stubs`: https://github.com/typeddjango/django-stubs
.. _`djangorestframework-stubs`: https://github.com/typeddjango/djangorestframework-stubs

Note, the django-configurations mypy plugin must come before plugins that
need it in your mypy configuration file. Example ``plugins`` value if configuring
mypy with ``pyproject.toml``:


.. code-block:: toml
   :emphasize-lines: 9, 11-12

    plugins = [
        "configurations.mypy_plugin",
        "mypy_django_plugin.main",
        "mypy_drf_plugin.main",
    ]

..
