.. :changelog:

Changelog
---------

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
