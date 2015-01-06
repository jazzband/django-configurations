import sys

from django.core.exceptions import ImproperlyConfigured
from django.utils import six
from django.utils.importlib import import_module


def isuppercase(name):
    return name == name.upper() and not name.startswith('_')


def uppercase_attributes(obj):
    return dict((name, getattr(obj, name))
                for name in filter(isuppercase, dir(obj)))


def import_by_path(dotted_path, error_prefix=''):
    """
    Import a dotted module path and return the attribute/class designated by
    the last name in the path. Raise ImproperlyConfigured if something goes
    wrong.

    Backported from Django 1.6.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        raise ImproperlyConfigured("{0}{1} doesn't look like "
                                   "a module path".format(error_prefix,
                                                          dotted_path))
    try:
        module = import_module(module_path)
    except ImportError as err:
        msg = '{0}Error importing module {1}: "{2}"'.format(error_prefix,
                                                            module_path,
                                                            err)
        six.reraise(ImproperlyConfigured, ImproperlyConfigured(msg),
                    sys.exc_info()[2])
    try:
        attr = getattr(module, class_name)
    except AttributeError:
        raise ImproperlyConfigured('{0}Module "{1}" does not define a '
                                   '"{2}" attribute/class'.format(error_prefix,
                                                                  module_path,
                                                                  class_name))
    return attr


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
    exc.args = ('{0} {1} {2}'.format(prefix, exc.args[0], suffix),) + args[1:]
    raise

try:
    from django.core.management import LaxOptionParser
except ImportError:
    from optparse import OptionParser

    class LaxOptionParser(OptionParser):
        """
        An option parser that doesn't raise any errors on unknown options.

        This is needed because the --settings and --pythonpath options affect
        the commands (and thus the options) that are available to the user.

        Backported from Django 1.7.x

        """
        def error(self, msg):
            pass

        def print_help(self):
            """Output nothing.

            The lax options are included in the normal option parser, so under
            normal usage, we don't need to print the lax options.
            """
            pass

        def print_lax_help(self):
            """Output the basic options available to every command.

            This just redirects to the default print_help() behavior.
            """
            OptionParser.print_help(self)

        def _process_args(self, largs, rargs, values):
            """
            Overrides OptionParser._process_args to exclusively handle default
            options and ignore args and other options.

            This overrides the behavior of the super class, which stop parsing
            at the first unrecognized option.
            """
            while rargs:
                arg = rargs[0]
                try:
                    if arg[0:2] == "--" and len(arg) > 2:
                        # process a single long option (possibly with value(s))
                        # the superclass code pops the arg off rargs
                        self._process_long_opt(rargs, values)
                    elif arg[:1] == "-" and len(arg) > 1:
                        # process a cluster of short options (possibly with
                        # value(s) for the last one only)
                        # the superclass code pops the arg off rargs
                        self._process_short_opts(rargs, values)
                    else:
                        # it's either a non-default option or an arg
                        # either way, add it to the args list so we can keep
                        # dealing with options
                        del rargs[0]
                        raise Exception
                except:  # Needed because we might need to catch a SystemExit
                    largs.append(arg)
