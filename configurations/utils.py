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
