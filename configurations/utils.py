import inspect
import sys
import warnings

from functools import partial
from importlib import import_module

from django.core.exceptions import ImproperlyConfigured


def isuppercase(name):
    return name == name.upper() and not name.startswith('_')


def uppercase_attributes(obj):
    return {name: getattr(obj, name) for name in dir(obj) if isuppercase(name)}


def import_by_path(dotted_path, error_prefix=''):
    """
    Import a dotted module path and return the attribute/class designated by
    the last name in the path. Raise ImproperlyConfigured if something goes
    wrong.

    Backported from Django 1.6.
    """
    warnings.warn("Function utils.import_by_path is deprecated in favor of "
                  "django.utils.module_loading.import_string.", DeprecationWarning)
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
        raise ImproperlyConfigured(msg).with_traceback(sys.exc_info()[2])
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
    exc.args = ('{0} {1} {2}'.format(prefix, args[0], suffix),) + args[1:]
    raise exc


# Copied over from Sphinx
def getargspec(func):
    """Like inspect.getargspec but supports functools.partial as well."""
    if inspect.ismethod(func):
        func = func.__func__
    if type(func) is partial:
        orig_func = func.func
        argspec = getargspec(orig_func)
        args = list(argspec[0])
        defaults = list(argspec[3] or ())
        kwoargs = list(argspec[4])
        kwodefs = dict(argspec[5] or {})
        if func.args:
            args = args[len(func.args):]
        for arg in func.keywords or ():
            try:
                i = args.index(arg) - len(args)
                del args[i]
                try:
                    del defaults[i]
                except IndexError:
                    pass
            except ValueError:   # must be a kwonly arg
                i = kwoargs.index(arg)
                del kwoargs[i]
                del kwodefs[arg]
        return inspect.FullArgSpec(args, argspec[1], argspec[2],
                                    tuple(defaults), kwoargs,
                                    kwodefs, argspec[6])
    while hasattr(func, '__wrapped__'):
        func = func.__wrapped__
    if not inspect.isfunction(func):
        raise TypeError('%r is not a Python function' % func)
    return inspect.getfullargspec(func)
