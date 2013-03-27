.. :changelog:

Changelog
---------

v0.3 (2013-03-27)
^^^^^^^^^^^^^^^^^

- **backward incompatible change** Dropped support for Python 2.5.

- Added Python>3.2 and Django 1.5 support!

- Catch error when getting or evaluating callable setting class attributes.

- Extended tests.

- Added ``-C``/``--configration`` option to management command base class
  to follow the example of the ``--settings`` option.

v0.2 (2012-09-21)
^^^^^^^^^^^^^^^^^

- Added optional ``--configuration`` management command option similar
  to Django's ``--settings`` option

- Fixed the runserver message about which setting is used to
  show the correct class

- Stopped hiding AttributeErrors happening during initialization
  of settings classes

- Simplified tests

- Minor documentation fixes

v0.1 (2012-07-21)
^^^^^^^^^^^^^^^^^

- Initial public release
