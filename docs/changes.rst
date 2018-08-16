.. :changelog:

Changelog
---------

v2.2 (2018-xx-yy)
^^^^^^^^^^^^^^^^^

- **BACKWARD INCOMPATIBLE** Drop support of Django < 1.11.

v2.1 (2018-08-16)
^^^^^^^^^^^^^^^^^

- **BACKWARD INCOMPATIBLE** Drop support of Python 3.3.

- **BACKWARD INCOMPATIBLE** Drop support of Django 1.9.

- Add support for Django 2.1.

- Add ``PositiveIntegerValue`` configuration value.

- Fix ``bool(BooleanValue)`` to behave as one would expect (e.g.
  ``bool(BooleanValue(False))`` returns ``False``).

- Miscellaneous documentation improvements and bug fixes.

v2.0 (2016-07-29)
^^^^^^^^^^^^^^^^^

- **BACKWARD INCOMPATIBLE** Drop support of Python 2.6 and 3.2

- **BACKWARD INCOMPATIBLE** Drop support of Django < 1.8

- **BACKWARD INCOMPATIBLE** Moved sphinx callable has been moved from
  ``configurations`` to ``configurations.sphinx``.

- **BACKWARD INCOMPATIBLE** Removed the previously deprecated
  ``configurations.Settings`` class in favor of the
  ``configurations.Configuration`` added in 0.4. This removal was planned for
  the 1.0 release and is now finally enacted.

- Add multiprocessing support for sphinx integration

- Fix a RemovedInDjango19Warning warning

v1.0 (2016-01-04)
^^^^^^^^^^^^^^^^^

- Project has moved to `Jazzband <https://jazzband.co/>`_. See guidelines for
  contributing.

- Support for Django 1.8 and above.

- Allow ``Value`` classes to be used outside of ``Configuration`` classes. (#62)

- Fixed "Value with ValidationMixin will raise ValueError if no default assigned". (#69)

- Fixed wrong behaviour when assigning BooleanValue. (#83)

- Add ability to programmatically call Django commands from configurations using
  ``call_command``.

- Added SingleNestedTupleValue and SingleNestedListValue classes. (#85)

- Several other miscellaneous bugfixes.

v0.8 (2014-01-16)
^^^^^^^^^^^^^^^^^

- Added ``SearchURLValue`` to configure Haystack ``HAYSTACK_CONNECTIONS``
  settings.

v0.7 (2013-11-26)
^^^^^^^^^^^^^^^^^

- Removed the broken stdout wrapper that displayed the currently enabled
  configuration when using the runserver management command. Added a logging
  based solution instead.

- Fixed default value of ``CacheURLValue`` class that was shadowed by an
  unneeded name parameter. Thanks to Stefan Wehrmeyer.

- Fixed command line options checking in the importer to happen before the
  validation. Thanks to Stefan Wehrmeyer.

- Added Tox test configuration.

- Fixed an erroneous use of ``PathValue`` in the 1.6.x project template.

v0.6 (2013-09-19)
^^^^^^^^^^^^^^^^^

- Added a IPython extension to support IPython notebooks correctly. See
  the :doc:`cookbook` for more information.

v0.5.1 (2013-09-12)
^^^^^^^^^^^^^^^^^^^

- Prevented accidentally parsing the command line options to look for the
  ``--configuration`` option outside of Django's management commands.
  This should fix a problem with gunicorn's own ``--config`` option.
  Thanks to Brian Rosner for the report.

v0.5 (2013-09-09)
^^^^^^^^^^^^^^^^^

- Switched from raising Django's ``ImproperlyConfigured`` exception on errors
  to standard ``ValueError`` to prevent hiding those errors when Django
  specially handles the first.

- Switched away from d2to1 as a way to define package metadata since distutils2
  is dead.

- Extended ``Value`` class documentation and fixed other issues.

- Moved tests out of the ``configurations`` package for easier maintenance.

v0.4 (2013-09-03)
^^^^^^^^^^^^^^^^^

- Added ``Value`` classes and subclasses for easier handling of settings values,
  including populating them from environment variables.

- Renamed ``configurations.Settings`` class to ``configurations.Configuration``
  to better describe what the class is all about. The old class still exists
  and is marked as pending deprecation. It'll be removed in version 1.0.

- Added a ``setup`` method to handle the new ``Value`` classes and allow an
  in-between modification of the configuration values.

- Added Django project templates for 1.5.x and 1.6.x.

- Reorganized and extended documentation.

v0.3.2 (2014-01-16)
^^^^^^^^^^^^^^^^^^^

- Fixed an installation issue.

v0.3.1 (2013-09-20)
^^^^^^^^^^^^^^^^^^^

- Backported a fix from master that makes 0.3.x compatible with newer
  versions of six.

v0.3 (2013-05-15)
^^^^^^^^^^^^^^^^^

- Added ``pristinemethod`` decorator to be able to have callables as settings.

- Added ``pre_setup`` and ``post_setup`` method hooks to be able to run code
  before or after the settings loading is finished.

- Minor docs and tests cleanup.

v0.2.1 (2013-04-11)
^^^^^^^^^^^^^^^^^^^

- Fixed a regression in parsing the new ``-C``/``--configuration`` management
  command option.

- Minor fix in showing the configuration in the ``runserver`` management
  command output.

v0.2 (2013-03-27)
^^^^^^^^^^^^^^^^^

- **backward incompatible change** Dropped support for Python 2.5! Please use
  the 0.1 version if you really want.

- Added Python>3.2 and Django 1.5 support!

- Catch error when getting or evaluating callable setting class attributes.

- Simplified and extended tests.

- Added optional ``-C``/``--configuration`` management command option similar
  to Django's ``--settings`` option

- Fixed the runserver message about which setting is used to
  show the correct class.

- Stopped hiding AttributeErrors happening during initialization
  of settings classes.

- Added FastCGI helper.

- Minor documentation fixes

v0.1 (2012-07-21)
^^^^^^^^^^^^^^^^^

- Initial public release
