import imp
import os
import sys

from django.core.exceptions import ImproperlyConfigured
from django.conf import ENVIRONMENT_VARIABLE

from .utils import uppercase_attributes


installed = False


def install():
    global installed
    if not installed:
        sys.meta_path.append(SettingsImporter())
        installed = True


class SettingsImporter(object):
    class_varname = 'DJANGO_CONFIGURATION'
    error_msg = "Settings cannot be imported, environment variable %s is undefined."

    def __init__(self):
        self.validate()

    def __repr__(self):
        return "<SettingsImporter for '%s.%s'>" % (self.module, self.name)

    @property
    def module(self):
        return os.environ.get(ENVIRONMENT_VARIABLE)

    @property
    def name(self):
        return os.environ.get(self.class_varname)

    def validate(self):
        if self.name is None:
            raise ImproperlyConfigured(self.error_msg % self.class_varname)
        if self.module is None:
            raise ImproperlyConfigured(self.error_msg % ENVIRONMENT_VARIABLE)

    def find_module(self, fullname, path=None):
        if fullname is not None and fullname == self.module:
            module = fullname.rsplit('.', 1)[-1]
            return SettingsLoader(self.name, imp.find_module(module, path))
        return None


class SettingsLoader(object):

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def load_module(self, fullname):
        if fullname in sys.modules:
            mod = sys.modules[fullname]  # pragma: no cover
        else:
            mod = imp.load_module(fullname, *self.location)
        try:
            cls = getattr(mod, self.name)
            obj = cls()
        except AttributeError:  # pragma: no cover
            raise ImproperlyConfigured("Couldn't find settings '%s' in "
                                       "module '%s'" %
                                       (self.name, mod.__package__))
        for name, value in uppercase_attributes(obj).items():
            if callable(value):
                value = value()
            setattr(mod, name, value)
        setattr(mod, 'CONFIGURATION', '%s.%s' % (fullname, self.name))
        return mod
