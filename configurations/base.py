import os
import re

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

        deprecated_settings = {
            # DEFAULT_HASHING_ALGORITHM is always deprecated, as it's a
            # transitional setting
            # https://docs.djangoproject.com/en/3.1/releases/3.1/#default-hashing-algorithm-settings
            "DEFAULT_HASHING_ALGORITHM",
            # DEFAULT_CONTENT_TYPE and FILE_CHARSET are deprecated in
            # Django 2.2 and are removed in Django 3.0
            "DEFAULT_CONTENT_TYPE",
            "FILE_CHARSET",
            # When DEFAULT_AUTO_FIELD is not explicitly set, Django's emits a
            # system check warning models.W042. This warning should not be
            # suppressed, as downstream users are expected to make a decision.
            # https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
            "DEFAULT_AUTO_FIELD",
        }
        # PASSWORD_RESET_TIMEOUT_DAYS is deprecated in favor of
        # PASSWORD_RESET_TIMEOUT in Django 3.1
        # https://github.com/django/django/commit/226ebb17290b604ef29e82fb5c1fbac3594ac163#diff-ec2bed07bb264cb95a80f08d71a47c06R163-R170
        if "PASSWORD_RESET_TIMEOUT" in settings_vars:
            deprecated_settings.add("PASSWORD_RESET_TIMEOUT_DAYS")
        # DEFAULT_FILE_STORAGE and STATICFILES_STORAGE are deprecated
        # in favor of STORAGES.
        # https://docs.djangoproject.com/en/dev/releases/4.2/#custom-file-storages
        if "STORAGES" in settings_vars:
            deprecated_settings.add("DEFAULT_FILE_STORAGE")
            deprecated_settings.add("STATICFILES_STORAGE")
        for deprecated_setting in deprecated_settings:
            if deprecated_setting in settings_vars:
                del settings_vars[deprecated_setting]
        attrs = {**settings_vars, **attrs}

        return super().__new__(cls, name, bases, attrs)

    def __repr__(self):
        return "<Configuration '{0}.{1}'>".format(self.__module__,
                                                  self.__name__)


class Configuration(metaclass=ConfigurationBase):
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
        # check if the class has DOTENV set whether with a path or None
        dotenv = getattr(cls, 'DOTENV', None)

        # if DOTENV is falsy we want to disable it
        if not dotenv:
            return

        # now check if we can access the file since we know we really want to
        try:
            with open(dotenv, 'r') as f:
                content = f.read()
        except OSError as e:
            raise ImproperlyConfigured("Couldn't read .env file "
                                       "with the path {}. Error: "
                                       "{}".format(dotenv, e)) from e
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
