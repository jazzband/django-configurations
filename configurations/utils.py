import inspect
import sys

from django.core.exceptions import ImproperlyConfigured
from django.utils import six
try:
    from importlib import import_module
except ImportError:
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


# Copied over from Sphinx
if sys.version_info >= (3, 0):
    from functools import partial

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

else:  # 2.6, 2.7
    from functools import partial

    def getargspec(func):
        """Like inspect.getargspec but supports functools.partial as well."""
        if inspect.ismethod(func):
            func = func.im_func
        parts = 0, ()
        if type(func) is partial:
            keywords = func.keywords
            if keywords is None:
                keywords = {}
            parts = len(func.args), keywords.keys()
            func = func.func
        if not inspect.isfunction(func):
            raise TypeError('%r is not a Python function' % func)
        args, varargs, varkw = inspect.getargs(func.func_code)
        func_defaults = func.func_defaults
        if func_defaults is None:
            func_defaults = []
        else:
            func_defaults = list(func_defaults)
        if parts[0]:
            args = args[parts[0]:]
        if parts[1]:
            for arg in parts[1]:
                i = args.index(arg) - len(args)
                del args[i]
                try:
                    del func_defaults[i]
                except IndexError:
                    pass
        return inspect.ArgSpec(args, varargs, varkw, func_defaults)
