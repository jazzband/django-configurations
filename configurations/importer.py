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

from .utils import uppercase_attributes, reraise
from .values import Value, setup_value

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
            new_msg_part = (", configuration {0!r}".format(
                            os.environ.get(CONFIGURATION_ENVIRONMENT_VARIABLE)))
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
                help='The name of the configuration class to load, e.g. '
                     '"Development". If this isn\'t provided, the '
                     'DJANGO_CONFIGURATION environment variable will '
                     'be used.'),)


def install(check_options=False):
    global installed
    if not installed:

        from django.core import management
        from django.core.management import base

        # add the configuration option to all management commands
        base.BaseCommand.option_list += configuration_options

        importer = ConfigurationImporter(check_options=check_options)
        sys.meta_path.insert(0, importer)
        installed = True

        # now patch the active runserver command to show a nicer output
        commands = management.get_commands()
        runserver = commands.get('runserver', None)
        if runserver is not None:
            path = '{0}.management.commands.runserver'.format(runserver)
            try:
                runserver_module = import_module(path)
            except ImportError:
                pass
            else:
                inner_run = runserver_module.Command.inner_run
                runserver_module.Command.inner_run = patch_inner_run(inner_run)


class ConfigurationImporter(object):
    modvar = SETTINGS_ENVIRONMENT_VARIABLE
    namevar = CONFIGURATION_ENVIRONMENT_VARIABLE
    error_msg = ("Configuration cannot be imported, "
                 "environment variable {0} is undefined.")

    def __init__(self, check_options=False):
        self.argv = sys.argv[:]
        if check_options:
            self.check_options()
        self.validate()

    def __repr__(self):
        return "<ConfigurationImporter for '{0}.{1}'>".format(self.module,
                                                              self.name)

    @property
    def module(self):
        return os.environ.get(self.modvar)

    @property
    def name(self):
        return os.environ.get(self.namevar)

    def check_options(self):
        parser = LaxOptionParser(option_list=configuration_options,
                                 add_help_option=False)
        try:
            options, args = parser.parse_args(self.argv)
            if options.configuration:
                os.environ[self.namevar] = options.configuration
        except:
            pass  # Ignore any option errors at this point.

    def validate(self):
        if self.name is None:
            raise ImproperlyConfigured(self.error_msg.format(self.namevar))
        if self.module is None:
            raise ImproperlyConfigured(self.error_msg.format(self.modvar))

    def find_module(self, fullname, path=None):
        if fullname is not None and fullname == self.module:
            module = fullname.rsplit('.', 1)[-1]
            return ConfigurationLoader(self.name,
                                       imp.find_module(module, path))
        return None


class ConfigurationLoader(object):

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def load_module(self, fullname):
        if fullname in sys.modules:
            mod = sys.modules[fullname]  # pragma: no cover
        else:
            mod = imp.load_module(fullname, *self.location)
        cls_path = '{0}.{1}'.format(mod.__name__, self.name)

        try:
            cls = getattr(mod, self.name)
        except AttributeError as err:  # pragma: no cover
            reraise(err, "Couldn't find configuration '{0}' "
                         "in module '{1}'".format(self.name,
                                                  mod.__package__))
        try:
            cls.pre_setup()
            cls.setup()
            obj = cls()
            attributes = uppercase_attributes(obj).items()
            for name, value in attributes:
                if callable(value) and not getattr(value, 'pristine', False):
                    value = value()
                    # in case a method returns a Value instance we have
                    # to do the same as the Configuration.setup method
                    if isinstance(value, Value):
                        setup_value(mod, name, value)
                        continue
                setattr(mod, name, value)

            setattr(mod, 'CONFIGURATION', '{0}.{1}'.format(fullname,
                                                           self.name))
            cls.post_setup()

        except Exception as err:
            reraise(err, "Couldn't setup configuration '{0}'".format(cls_path))

        return mod
