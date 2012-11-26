import imp
import os
import sys
from functools import wraps
from optparse import make_option

import django
from django.core import management
from django.core.management import base
from django.core.exceptions import ImproperlyConfigured
from django.conf import ENVIRONMENT_VARIABLE
from django.utils.decorators import available_attrs
from django.utils.importlib import import_module

from .utils import uppercase_attributes


installed = False


def patch_handle_default_options(original):
    @wraps(original, assigned=available_attrs(original))
    def handle_default_options(options):
        """
        Include any default options that all commands should accept here
        so that ManagementUtility can handle them before searching for
        user commands.

        """
        original(options)
        if options.configuration:
            os.environ[SettingsImporter.class_varname] = options.configuration
    return handle_default_options


class StdoutWrapper(object):
    """
    Wrap the stdout to patch one line, yup.
    """
    def __init__(self, out):
        self._out = out

    def __getattr__(self, name):
        return getattr(self._out, name)

    def write(self, msg, *args, **kwargs):
        if msg.startswith('Django version'):
            from django.conf import settings
            msg_parts = msg.split('\n')
            msg_parts[0] = ("Django version %s, using settings %r" %
                            (django.get_version(), settings.CONFIGURATION))
            msg = '\n'.join(msg_parts)
        return self._out.write(msg, *args, **kwargs)


def patch_inner_run(original):
    @wraps(original, assigned=available_attrs(original))
    def inner_run(self, *args, **options):
        if hasattr(self, 'stdout'):
            self.stdout = StdoutWrapper(self.stdout)
        return original(self, *args, **options)
    return inner_run


def install():
    global installed
    if not installed:

        # add the configuration option to all management commands
        original = base.handle_default_options
        patched = patch_handle_default_options(original)
        base.handle_default_options = patched
        management.handle_default_options = patched
        base.BaseCommand.option_list += (
            make_option('-C', '--configuration',
                        help='The name of the settings class to load, e.g. '
                             '"Development". If this isn\'t provided, the '
                             'DJANGO_CONFIGURATION environment variable will '
                             'be used.'),)

        sys.meta_path.append(SettingsImporter())
        installed = True

        # now patch the active runserver command to show a nicer output
        commands = management.get_commands()
        runserver_path = commands.get('runserver', None)
        if runserver_path is not None:
            full_path = '%s.management.commands.runserver' % runserver_path
            try:
                runserver_module = import_module(full_path)
            except ImportError:
                pass
            else:
                original_inner_run = runserver_module.Command.inner_run
                runserver_module.Command.inner_run = patch_inner_run(original_inner_run)


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
        except AttributeError:  # pragma: no cover
            raise ImproperlyConfigured("Couldn't find settings '%s' in "
                                       "module '%s'" %
                                       (self.name, mod.__package__))
        try:
            obj = cls()
        except Exception, err:
            raise ImproperlyConfigured("Couldn't load settings '%s.%s': %s" %
                                       (mod.__name__, self.name, err))
        try:
            attributes = uppercase_attributes(obj).items()
        except Exception, err:
            raise ImproperlyConfigured("Couldn't get items of settings '%s.%s': %s" %
                                       (mod.__name__, self.name, err))
        for name, value in attributes:
            if callable(value):
                try:
                    value = value()
                except Exception, err:
                    raise ImproperlyConfigured(
                        "Couldn't execute callable '%s' in '%s.%s': %s" %
                        (value, mod.__name__, self.name, err))
                setattr(mod, name, value)
        setattr(mod, 'CONFIGURATION', '%s.%s' % (fullname, self.name))
        return mod
