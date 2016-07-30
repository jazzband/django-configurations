import os
import re

from django.utils import six
from django.conf import global_settings
from django.core.exceptions import ImproperlyConfigured

from .utils import uppercase_attributes
from .values import Value, setup_value

__all__ = ['Configuration']


install_failure = ("django-configurations settings importer wasn't "
                   "correctly installed. Please use one of the starter "
                   "functions to install it as mentioned in the docs: "
                   "https://django-configurations.readthedocs.io/")


class ConfigurationBase(type):

    def __new__(cls, name, bases, attrs):
        if bases not in ((object,), ()) and bases[0].__name__ != 'NewBase':
            # if this is actually a subclass in a settings module
            # we better check if the importer was correctly installed
            from . import importer
            if not importer.installed:
                raise ImproperlyConfigured(install_failure)
        settings_vars = uppercase_attributes(global_settings)
        parents = [base for base in bases if isinstance(base,
                                                        ConfigurationBase)]
        if parents:
            for base in bases[::-1]:
                settings_vars.update(uppercase_attributes(base))
        attrs = dict(settings_vars, **attrs)
        return super(ConfigurationBase, cls).__new__(cls, name, bases, attrs)

    def __repr__(self):
        return "<Configuration '{0}.{1}'>".format(self.__module__,
                                                  self.__name__)


class Configuration(six.with_metaclass(ConfigurationBase)):
    """
    The base configuration class to inherit from.

    ::

        class Develop(Configuration):
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
    DOTENV_LOADED = None

    @classmethod
    def load_dotenv(cls):
        """
        Pulled from Honcho code with minor updates, reads local default
        environment variables from a .env file located in the project root
        or provided directory.

        http://www.wellfireinteractive.com/blog/easier-12-factor-django/
        https://gist.github.com/bennylope/2999704
        """
        # check if the class has DOTENV set wether with a path or None
        dotenv = getattr(cls, 'DOTENV', None)

        # if DOTENV is falsy we want to disable it
        if not dotenv:
            return

        # now check if we can access the file since we know we really want to
        try:
            with open(dotenv, 'r') as f:
                content = f.read()
        except IOError as e:
            raise ImproperlyConfigured("Couldn't read .env file "
                                       "with the path {}. Error: "
                                       "{}".format(dotenv, e))
        else:
            for line in content.splitlines():
                m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
                if not m1:
                    continue
                key, val = m1.group(1), m1.group(2)
                m2 = re.match(r"\A'(.*)'\Z", val)
                if m2:
                    val = m2.group(1)
                m3 = re.match(r'\A"(.*)"\Z', val)
                if m3:
                    val = re.sub(r'\\(.)', r'\1', m3.group(1))
                os.environ.setdefault(key, val)

            cls.DOTENV_LOADED = dotenv

    @classmethod
    def pre_setup(cls):
        if cls.DOTENV_LOADED is None:
            cls.load_dotenv()

    @classmethod
    def post_setup(cls):
        pass

    @classmethod
    def setup(cls):
        for name, value in uppercase_attributes(cls).items():
            if isinstance(value, Value):
                setup_value(cls, name, value)
