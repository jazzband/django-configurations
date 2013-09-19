.. :changelog:

Changelog
---------

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
