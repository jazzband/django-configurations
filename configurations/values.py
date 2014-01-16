import ast
import copy
import decimal
import os
import sys

from django.core import validators
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.utils import six

from .utils import import_by_path


def setup_value(target, name, value):
    actual_value = value.setup(name)
    # overwriting the original Value class with the result
    setattr(target, name, actual_value)
    if value.multiple:
        for multiple_name, multiple_value in actual_value.items():
            setattr(target, multiple_name, multiple_value)


class Value(object):
    """
    A single settings value that is able to interpret env variables
    and implements a simple validation scheme.
    """
    multiple = False

    def __init__(self, default=None, environ=True, environ_name=None,
                 environ_prefix='DJANGO', *args, **kwargs):
        if isinstance(default, Value):
            self.default = copy.copy(default.default)
        else:
            self.default = default
        self.environ = environ
        if environ_prefix and environ_prefix.endswith('_'):
            environ_prefix = environ_prefix[:-1]
        self.environ_prefix = environ_prefix
        self.environ_name = environ_name

    def __repr__(self):
        return "<Value default: {0}>".format(self.default)

    def setup(self, name):
        value = self.default
        if self.environ:
            if self.environ_name is None:
                environ_name = name.upper()
            else:
                environ_name = self.environ_name
            if self.environ_prefix:
                full_environ_name = '{0}_{1}'.format(self.environ_prefix,
                                                     environ_name)
            else:
                full_environ_name = environ_name
            if full_environ_name in os.environ:
                value = self.to_python(os.environ[full_environ_name])
        return value

    def to_python(self, value):
        """
        Convert the given value of a environment variable into an
        appropriate Python representation of the value.
        This should be overriden when subclassing.
        """
        return value


class MultipleMixin(object):
    multiple = True


class BooleanValue(Value):
    true_values = ('yes', 'y', 'true', '1')
    false_values = ('no', 'n', 'false', '0', '')

    def __init__(self, *args, **kwargs):
        super(BooleanValue, self).__init__(*args, **kwargs)
        if self.default not in (True, False):
            raise ValueError('Default value {0!r} is not a '
                             'boolean value'.format(self.default))

    def to_python(self, value):
        normalized_value = value.strip().lower()
        if normalized_value in self.true_values:
            return True
        elif normalized_value in self.false_values:
            return False
        else:
            raise ValueError('Cannot interpret '
                             'boolean value {0!r}'.format(value))


class CastingMixin(object):
    exception = (TypeError, ValueError)
    message = 'Cannot interpret value {0!r}'

    def __init__(self, *args, **kwargs):
        super(CastingMixin, self).__init__(*args, **kwargs)
        if isinstance(self.caster, six.string_types):
            self._caster = import_by_path(self.caster)
        elif callable(self.caster):
            self._caster = self.caster
        else:
            error = 'Cannot use caster of {0} ({1!r})'.format(self,
                                                              self.caster)
            raise ValueError(error)

    def to_python(self, value):
        try:
            return self._caster(value)
        except self.exception:
            raise ValueError(self.message.format(value))


class IntegerValue(CastingMixin, Value):
    caster = int


class FloatValue(CastingMixin, Value):
    caster = float


class DecimalValue(CastingMixin, Value):
    caster = decimal.Decimal
    exception = decimal.InvalidOperation


class ListValue(Value):
    converter = None
    message = 'Cannot interpret list item {0!r} in list {1!r}'

    def __init__(self, *args, **kwargs):
        self.separator = kwargs.pop('separator', ',')
        converter = kwargs.pop('converter', None)
        if converter is not None:
            self.converter = converter
        super(ListValue, self).__init__(*args, **kwargs)
        # make sure the default is a list
        if self.default is None:
            self.default = []
        # initial conversion
        if self.converter is not None:
            self.default = [self.converter(value) for value in self.default]

    def to_python(self, value):
        split_value = [v.strip() for v in value.strip().split(self.separator)]
        # removing empty items
        value_list = filter(None, split_value)
        if self.converter is None:
            return list(value_list)

        converted_values = []
        for list_value in value_list:
            try:
                converted_values.append(self.converter(list_value))
            except (TypeError, ValueError):
                raise ValueError(self.message.format(list_value, value))
        return converted_values


class BackendsValue(ListValue):

    def converter(self, value):
        try:
            import_by_path(value)
        except ImproperlyConfigured as err:
            six.reraise(ValueError, ValueError(err), sys.exc_info()[2])
        return value


class TupleValue(ListValue):
    message = 'Cannot interpret tuple item {0!r} in tuple {1!r}'

    def __init__(self, *args, **kwargs):
        super(TupleValue, self).__init__(*args, **kwargs)
        if self.default is None:
            self.default = ()
        else:
            self.default = tuple(self.default)

    def to_python(self, value):
        return tuple(super(TupleValue, self).to_python(value))


class SetValue(ListValue):
    message = 'Cannot interpret set item {0!r} in set {1!r}'

    def __init__(self, *args, **kwargs):
        super(SetValue, self).__init__(*args, **kwargs)
        if self.default is None:
            self.default = set()
        else:
            self.default = set(self.default)

    def to_python(self, value):
        return set(super(SetValue, self).to_python(value))


class DictValue(Value):
    message = 'Cannot interpret dict value {0!r}'

    def __init__(self, *args, **kwargs):
        super(DictValue, self).__init__(*args, **kwargs)
        if self.default is None:
            self.default = {}
        else:
            self.default = dict(self.default)

    def to_python(self, value):
        value = super(DictValue, self).to_python(value)
        if not value:
            return {}
        try:
            evaled_value = ast.literal_eval(value)
        except ValueError:
            raise ValueError(self.message.format(value))
        if not isinstance(evaled_value, dict):
            raise ValueError(self.message.format(value))
        return evaled_value


class ValidationMixin(object):

    def __init__(self, *args, **kwargs):
        super(ValidationMixin, self).__init__(*args, **kwargs)
        if isinstance(self.validator, six.string_types):
            self._validator = import_by_path(self.validator)
        elif callable(self.validator):
            self._validator = self.validator
        else:
            raise ValueError('Cannot use validator of '
                             '{0} ({1!r})'.format(self, self.validator))
        self.to_python(self.default)

    def to_python(self, value):
        try:
            self._validator(value)
        except ValidationError:
            raise ValueError(self.message.format(value))
        else:
            return value


class EmailValue(ValidationMixin, Value):
    message = 'Cannot interpret email value {0!r}'
    validator = 'django.core.validators.validate_email'


class URLValue(ValidationMixin, Value):
    message = 'Cannot interpret URL value {0!r}'
    validator = validators.URLValidator()


class IPValue(ValidationMixin, Value):
    message = 'Cannot interpret IP value {0!r}'
    validator = 'django.core.validators.validate_ipv46_address'


class RegexValue(ValidationMixin, Value):
    message = "Regex doesn't match value {0!r}"

    def __init__(self, *args, **kwargs):
        regex = kwargs.pop('regex', None)
        self.validator = validators.RegexValidator(regex=regex)
        super(RegexValue, self).__init__(*args, **kwargs)


class PathValue(Value):
    def __init__(self, *args, **kwargs):
        self.check_exists = kwargs.pop('check_exists', True)
        super(PathValue, self).__init__(*args, **kwargs)

    def setup(self, name):
        value = super(PathValue, self).setup(name)
        value = os.path.expanduser(value)
        if self.check_exists and not os.path.exists(value):
            raise ValueError('Path {0!r} does  not exist.'.format(value))
        return os.path.abspath(value)


class SecretValue(Value):

    def __init__(self, *args, **kwargs):
        kwargs['environ'] = True
        super(SecretValue, self).__init__(*args, **kwargs)
        if self.default is not None:
            raise ValueError('Secret values are only allowed to '
                             'be set as environment variables')

    def setup(self, name):
        value = super(SecretValue, self).setup(name)
        if not value:
            raise ValueError('Secret value {0!r} is not set'.format(name))
        return value


class EmailURLValue(CastingMixin, MultipleMixin, Value):
    caster = 'dj_email_url.parse'
    message = 'Cannot interpret email URL value {0!r}'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('environ', True)
        kwargs.setdefault('environ_prefix', None)
        kwargs.setdefault('environ_name', 'EMAIL_URL')
        super(EmailURLValue, self).__init__(*args, **kwargs)
        if self.default is None:
            self.default = {}
        else:
            self.default = self.to_python(self.default)


class DictBackendMixin(Value):
    default_alias = 'default'

    def __init__(self, *args, **kwargs):
        self.alias = kwargs.pop('alias', self.default_alias)
        kwargs.setdefault('environ', True)
        kwargs.setdefault('environ_prefix', None)
        kwargs.setdefault('environ_name', self.environ_name)
        super(DictBackendMixin, self).__init__(*args, **kwargs)
        if self.default is None:
            self.default = {}
        else:
            self.default = self.to_python(self.default)

    def to_python(self, value):
        value = super(DictBackendMixin, self).to_python(value)
        return {self.alias: value}


class DatabaseURLValue(DictBackendMixin, CastingMixin, Value):
    caster = 'dj_database_url.parse'
    message = 'Cannot interpret database URL value {0!r}'
    environ_name = 'DATABASE_URL'


class CacheURLValue(DictBackendMixin, CastingMixin, Value):
    caster = 'django_cache_url.parse'
    message = 'Cannot interpret cache URL value {0!r}'
    environ_name = 'CACHE_URL'


class SearchURLValue(DictBackendMixin, CastingMixin, Value):
    caster = 'dj_search_url.parse'
    message = 'Cannot interpret Search URL value {0!r}'
    environ_name = 'SEARCH_URL'
