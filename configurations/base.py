import six
from django.conf import global_settings
from django.core.exceptions import ImproperlyConfigured

from .utils import uppercase_attributes

__all__ = ['Settings']


install_failure = ("django-configurations settings importer wasn't "
                   "correctly installed. Please use one of the starter "
                   "functions to install it as mentioned in the docs: "
                   "http://django-configurations.readthedocs.org/")


class SettingsBase(type):

    def __new__(cls, name, bases, attrs):
        if bases not in ((object,), ()) and bases[0].__name__ != 'NewBase':
            # if this is actually a subclass in a settings module
            # we better check if the importer was correctly installed
            from . import importer
            if not importer.installed:
                raise ImproperlyConfigured(install_failure)
        settings_vars = uppercase_attributes(global_settings)
        parents = [base for base in bases if isinstance(base, SettingsBase)]
        if parents:
            for base in bases[::-1]:
                settings_vars.update(uppercase_attributes(base))
        attrs = dict(settings_vars, **attrs)
        return super(SettingsBase, cls).__new__(cls, name, bases, attrs)

    def __repr__(self):
        return "<Settings '%s.%s'>" % (self.__module__, self.__name__)


class Settings(six.with_metaclass(SettingsBase)):
    """
    The base configuration class to inherit from.

    ::

        class Develop(Settings):
            EXTRA_AWESOME = True

            @property
            def SOMETHING(self):
                return completely.different()

            def OTHER(self):
                if whatever:
                    return (1, 2, 3)
                return (4, 5, 6)

    The module this configuration class is located in will
    automatically get the class and instance level attributes
    with upper characters if the ``DJANGO_CONFIGURATION`` is set
    to the name of the class.

    """
    @classmethod
    def pre_setup(cls):
        pass

    @classmethod
    def post_setup(cls):
        pass
