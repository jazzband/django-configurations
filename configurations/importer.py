import imp
import logging
import os
import sys
from optparse import OptionParser, make_option

from django.conf import ENVIRONMENT_VARIABLE as SETTINGS_ENVIRONMENT_VARIABLE
from django.core.exceptions import ImproperlyConfigured
from django.core.management import base

from .utils import uppercase_attributes, reraise
from .values import Value, setup_value

installed = False

CONFIGURATION_ENVIRONMENT_VARIABLE = 'DJANGO_CONFIGURATION'
CONFIGURATION_ARGUMENT = '--configuration'
CONFIGURATION_ARGUMENT_HELP = ('The name of the configuration class to load, '
                               'e.g. "Development". If this isn\'t provided, '
                               'the  DJANGO_CONFIGURATION environment '
                               'variable will be used.')


configuration_options = (make_option(CONFIGURATION_ARGUMENT,
                                     help=CONFIGURATION_ARGUMENT_HELP),)


def install(check_options=False):
    global installed
    if not installed:
        orig_create_parser = base.BaseCommand.create_parser

        def create_parser(self, prog_name, subcommand):
            parser = orig_create_parser(self, prog_name, subcommand)
            if isinstance(parser, OptionParser):
                # in case the option_list is set the create_parser
                # will actually return a OptionParser for backward
                # compatibility. In that case we should tack our
                # options on to the end of the parser on the way out.
                for option in configuration_options:
                    parser.add_option(option)
            else:
                # probably argparse, let's not import argparse though
                parser.add_argument(CONFIGURATION_ARGUMENT,
                                    help=CONFIGURATION_ARGUMENT_HELP)
            return parser

        base.BaseCommand.create_parser = create_parser
        importer = ConfigurationImporter(check_options=check_options)
        sys.meta_path.insert(0, importer)
        installed = True


class ConfigurationImporter(object):
    modvar = SETTINGS_ENVIRONMENT_VARIABLE
    namevar = CONFIGURATION_ENVIRONMENT_VARIABLE
    error_msg = ("Configuration cannot be imported, "
                 "environment variable {0} is undefined.")

    def __init__(self, check_options=False):
        self.argv = sys.argv[:]
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        self.logger.addHandler(handler)
        if check_options:
            self.check_options()
        self.validate()
        if check_options:
            self.announce()

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
        try:
            parser = base.CommandParser(
                usage="%(prog)s subcommand [options] [args]",
                add_help=False)
        except TypeError:
            # Django before 2.1 used a `cmd` argument.
            parser = base.CommandParser(
                None,
                usage="%(prog)s subcommand [options] [args]",
                add_help=False)
        parser.add_argument('--settings')
        parser.add_argument('--pythonpath')
        parser.add_argument(CONFIGURATION_ARGUMENT,
                            help=CONFIGURATION_ARGUMENT_HELP)

        parser.add_argument('args', nargs='*')  # catch-all
        try:
            options, args = parser.parse_known_args(self.argv[2:])
            if options.configuration:
                os.environ[self.namevar] = options.configuration
            base.handle_default_options(options)
        except base.CommandError:
            pass  # Ignore any option errors at this point.

    def validate(self):
        if self.name is None:
            raise ImproperlyConfigured(self.error_msg.format(self.namevar))
        if self.module is None:
            raise ImproperlyConfigured(self.error_msg.format(self.modvar))

    def announce(self):
        if len(self.argv) > 1:
            from . import __version__
            from django.utils.termcolors import colorize
            from django.core.management.color import no_style

            if '--no-color' in self.argv:
                stylize = no_style()
            else:
                def stylize(text):
                    return colorize(text, fg='green')

            if (self.argv[1] == 'runserver' and
                    os.environ.get('RUN_MAIN') == 'true'):

                message = ("django-configurations version {0}, using "
                           "configuration '{1}'".format(__version__,
                                                        self.name))
                self.logger.debug(stylize(message))

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
