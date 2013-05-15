import imp
import os
import sys
from functools import wraps
from optparse import make_option

from django.core.exceptions import ImproperlyConfigured
from django.core.management import LaxOptionParser
from django.conf import ENVIRONMENT_VARIABLE as SETTINGS_ENVIRONMENT_VARIABLE
from django.utils.decorators import available_attrs
from django.utils.importlib import import_module

from .utils import uppercase_attributes


installed = False

CONFIGURATION_ENVIRONMENT_VARIABLE = 'DJANGO_CONFIGURATION'


class StdoutWrapper(object):
    """
    Wrap the stdout to patch one line, yup.
    """
    def __init__(self, out):
        self._out = out

    def __getattr__(self, name):
        return getattr(self._out, name)

    def write(self, msg, *args, **kwargs):
        if 'Django version' in msg:
            new_msg_part = (", configuration %r" %
                            os.environ.get(CONFIGURATION_ENVIRONMENT_VARIABLE))
            msg_parts = msg.split('\n')
            modified_msg_parts = []
            for msg_part in msg_parts:
                if msg_part.startswith('Django version'):
                    modified_msg_parts.append(msg_part + new_msg_part)
                else:
                    modified_msg_parts.append(msg_part)
            msg = '\n'.join(modified_msg_parts)
        return self._out.write(msg, *args, **kwargs)


def patch_inner_run(original):
    @wraps(original, assigned=available_attrs(original))
    def inner_run(self, *args, **options):
        if hasattr(self, 'stdout'):
            self.stdout = StdoutWrapper(self.stdout)
        return original(self, *args, **options)
    return inner_run

configuration_options = (
    make_option('--configuration',
                help='The name of the settings class to load, e.g. '
                     '"Development". If this isn\'t provided, the '
                     'DJANGO_CONFIGURATION environment variable will '
                     'be used.'),)


def install():
    global installed
    if not installed:

        from django.core import management
        from django.core.management import base

        # add the configuration option to all management commands
        base.BaseCommand.option_list += configuration_options

        sys.meta_path.insert(0, SettingsImporter())
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
                inner_run = runserver_module.Command.inner_run
                runserver_module.Command.inner_run = patch_inner_run(inner_run)


def handle_configurations_option(options):
    if options.configuration:
        os.environ[CONFIGURATION_ENVIRONMENT_VARIABLE] = options.configuration


class SettingsImporter(object):
    error_msg = ("Settings cannot be imported, "
                 "environment variable %s is undefined.")

    def __init__(self):
        self.argv = sys.argv[:]
        parser = LaxOptionParser(option_list=configuration_options,
                                 add_help_option=False)
        try:
            options, args = parser.parse_args(self.argv)
            handle_configurations_option(options)
        except:
            pass  # Ignore any option errors at this point.
        self.validate()

    def __repr__(self):
        return "<SettingsImporter for '%s.%s'>" % (self.module, self.name)

    @property
    def module(self):
        return os.environ.get(SETTINGS_ENVIRONMENT_VARIABLE)

    @property
    def name(self):
        return os.environ.get(CONFIGURATION_ENVIRONMENT_VARIABLE)

    def validate(self):
        if self.name is None:
            raise ImproperlyConfigured(self.error_msg %
                                       CONFIGURATION_ENVIRONMENT_VARIABLE)
        if self.module is None:
            raise ImproperlyConfigured(self.error_msg %
                                       SETTINGS_ENVIRONMENT_VARIABLE)

    def find_module(self, fullname, path=None):
        if fullname is not None and fullname == self.module:
            module = fullname.rsplit('.', 1)[-1]
            return SettingsLoader(self.name, imp.find_module(module, path))
        return None


def reraise(exc, prefix=None, suffix=None):
    args = exc.args
    if not args:
        args = ('',)
    if prefix is None:
        prefix = ''
    elif not prefix.endswith((':', ': ')):
        prefix = prefix + ': '
    if suffix is None:
        suffix = ''
    elif not (suffix.startswith('(') and suffix.endswith(')')):
        suffix = '(' + suffix + ')'
    exc.args = ('%s %s %s' % (prefix, exc.args[0], suffix),) + args[1:]
    raise


class SettingsLoader(object):

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def load_module(self, fullname):
        if fullname in sys.modules:
            mod = sys.modules[fullname]  # pragma: no cover
        else:
            mod = imp.load_module(fullname, *self.location)
        cls_path = '%s.%s' % (mod.__name__, self.name)

        try:
            cls = getattr(mod, self.name)
        except AttributeError as err:  # pragma: no cover
            reraise(err,
                    "While trying to find the '%s' settings in module '%s'" %
                    (self.name, mod.__package__))
        try:
            cls.pre_setup()
        except Exception as err:
            reraise(err, "While calling '%s.pre_setup()'" % cls_path)

        try:
            obj = cls()
        except Exception as err:
            reraise(err,
                    "While loading the '%s' settings" % cls_path)

        try:
            attributes = uppercase_attributes(obj).items()
        except Exception as err:
            reraise(err,
                    "While getting the items of the '%s' settings" %
                    cls_path)

        for name, value in attributes:
            if callable(value) and not getattr(value, 'pristine', False):
                try:
                    value = value()
                except Exception as err:
                    reraise(err,
                            "While calling '%s.%s'" % (cls_path, value))
            setattr(mod, name, value)

        setattr(mod, 'CONFIGURATION', '%s.%s' % (fullname, self.name))

        try:
            cls.post_setup()
        except Exception as err:
            reraise(err, "While calling '%s.post_setup()'" % cls_path)

        return mod
