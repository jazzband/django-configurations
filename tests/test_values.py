import decimal
import os
from contextlib import contextmanager

from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from unittest.mock import patch

from configurations.values import (Value, BooleanValue, IntegerValue,
                                   FloatValue, DecimalValue, ListValue,
                                   TupleValue, SingleNestedTupleValue,
                                   SingleNestedListValue, SetValue,
                                   DictValue, URLValue, EmailValue, IPValue,
                                   RegexValue, PathValue, SecretValue,
                                   DatabaseURLValue, EmailURLValue,
                                   CacheURLValue, BackendsValue,
                                   CastingMixin, SearchURLValue,
                                   setup_value, PositiveIntegerValue)


@contextmanager
def env(**kwargs):
    with patch.dict(os.environ, clear=True, **kwargs):
        yield


class FailingCasterValue(CastingMixin, Value):
    caster = 'non.existing.caster'


class ValueTests(TestCase):

    def test_value_with_default(self):
        value = Value('default', environ=False)
        self.assertEqual(type(value), type('default'))
        self.assertEqual(value, 'default')
        self.assertEqual(str(value), 'default')

    def test_value_with_default_and_late_binding(self):
        value = Value('default', environ=False, late_binding=True)
        self.assertEqual(type(value), Value)
        with env(DJANGO_TEST='override'):
            self.assertEqual(value.setup('TEST'), 'default')
            value = Value(environ_name='TEST')
            self.assertEqual(type(value), type('override'))
            self.assertEqual(value, 'override')
            self.assertEqual(str(value), 'override')
            self.assertEqual('{0}'.format(value), 'override')
            self.assertEqual('%s' % value, 'override')

            value = Value(environ_name='TEST', late_binding=True)
            self.assertEqual(type(value), Value)
            self.assertEqual(value.value, 'override')
            self.assertEqual(str(value), 'override')
            self.assertEqual('{0}'.format(value), 'override')
            self.assertEqual('%s' % value, 'override')

            self.assertEqual(repr(value), repr('override'))

    def test_value_truthy(self):
        value = Value('default')
        self.assertTrue(bool(value))

    def test_value_falsey(self):
        value = Value()
        self.assertFalse(bool(value))

    @patch.dict(os.environ, clear=True, DJANGO_TEST='override')
    def test_env_var(self):
        value = Value('default')
        self.assertEqual(value.setup('TEST'), 'override')
        self.assertEqual(str(value), 'override')
        self.assertNotEqual(value.setup('TEST'), value.default)
        self.assertEqual(value.to_python(os.environ['DJANGO_TEST']),
                         value.setup('TEST'))

    def test_value_reuse(self):
        value1 = Value('default')
        value2 = Value(value1)
        self.assertEqual(value1.setup('TEST1'), 'default')
        self.assertEqual(value2.setup('TEST2'), 'default')
        with env(DJANGO_TEST1='override1', DJANGO_TEST2='override2'):
            self.assertEqual(value1.setup('TEST1'), 'override1')
            self.assertEqual(value2.setup('TEST2'), 'override2')

    def test_value_var_equal(self):
        value1 = Value('default')
        value2 = Value('default')
        self.assertEqual(value1, value2)
        self.assertTrue(value1 in ['default'])

    def test_env_var_prefix(self):
        with patch.dict(os.environ, clear=True, ACME_TEST='override'):
            value = Value('default', environ_prefix='ACME')
            self.assertEqual(value.setup('TEST'), 'override')

        with patch.dict(os.environ, clear=True, TEST='override'):
            value = Value('default', environ_prefix='')
            self.assertEqual(value.setup('TEST'), 'override')

        with patch.dict(os.environ, clear=True, ACME_TEST='override'):
            value = Value('default', environ_prefix='ACME_')
            self.assertEqual(value.setup('TEST'), 'override')

    def test_boolean_values_true(self):
        value = BooleanValue(False)
        for truthy in value.true_values:
            with env(DJANGO_TEST=truthy):
                self.assertTrue(bool(value.setup('TEST')))

    def test_boolean_values_faulty(self):
        self.assertRaises(ValueError, BooleanValue, 'false')

    def test_boolean_values_false(self):
        value = BooleanValue(True)
        for falsy in value.false_values:
            with env(DJANGO_TEST=falsy):
                self.assertFalse(bool(value.setup('TEST')))

    def test_boolean_values_nonboolean(self):
        value = BooleanValue(True)
        with env(DJANGO_TEST='nonboolean'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_boolean_values_assign_false_to_another_booleanvalue(self):
        value1 = BooleanValue(False)
        value2 = BooleanValue(value1)
        self.assertFalse(value1.setup('TEST1'))
        self.assertFalse(value2.setup('TEST2'))

    def test_integer_values(self):
        value = IntegerValue(1)
        with env(DJANGO_TEST='2'):
            self.assertEqual(value.setup('TEST'), 2)
        with env(DJANGO_TEST='noninteger'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_positive_integer_values(self):
        value = PositiveIntegerValue(1)
        with env(DJANGO_TEST='2'):
            self.assertEqual(value.setup('TEST'), 2)
        with env(DJANGO_TEST='noninteger'):
            self.assertRaises(ValueError, value.setup, 'TEST')
        with env(DJANGO_TEST='-1'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_float_values(self):
        value = FloatValue(1.0)
        with env(DJANGO_TEST='2.0'):
            self.assertEqual(value.setup('TEST'), 2.0)
        with env(DJANGO_TEST='noninteger'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_decimal_values(self):
        value = DecimalValue(decimal.Decimal(1))
        with env(DJANGO_TEST='2'):
            self.assertEqual(value.setup('TEST'), decimal.Decimal(2))
        with env(DJANGO_TEST='nondecimal'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_failing_caster(self):
        self.assertRaises(ImproperlyConfigured, FailingCasterValue)

    def test_list_values_default(self):
        value = ListValue()
        with env(DJANGO_TEST='2,2'):
            self.assertEqual(value.setup('TEST'), ['2', '2'])
        with env(DJANGO_TEST='2, 2 ,'):
            self.assertEqual(value.setup('TEST'), ['2', '2'])
        with env(DJANGO_TEST=''):
            self.assertEqual(value.setup('TEST'), [])

    def test_list_values_separator(self):
        value = ListValue(separator=':')
        with env(DJANGO_TEST='/usr/bin:/usr/sbin:/usr/local/bin'):
            self.assertEqual(value.setup('TEST'),
                             ['/usr/bin', '/usr/sbin', '/usr/local/bin'])

    def test_List_values_converter(self):
        value = ListValue(converter=int)
        with env(DJANGO_TEST='2,2'):
            self.assertEqual(value.setup('TEST'), [2, 2])

        value = ListValue(converter=float)
        with env(DJANGO_TEST='2,2'):
            self.assertEqual(value.setup('TEST'), [2.0, 2.0])

    def test_list_values_custom_converter(self):
        value = ListValue(converter=lambda x: x * 2)
        with env(DJANGO_TEST='2,2'):
            self.assertEqual(value.setup('TEST'), ['22', '22'])

    def test_list_values_converter_exception(self):
        value = ListValue(converter=int)
        with env(DJANGO_TEST='2,b'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_tuple_values_default(self):
        value = TupleValue()
        with env(DJANGO_TEST='2,2'):
            self.assertEqual(value.setup('TEST'), ('2', '2'))
        with env(DJANGO_TEST='2, 2 ,'):
            self.assertEqual(value.setup('TEST'), ('2', '2'))
        with env(DJANGO_TEST=''):
            self.assertEqual(value.setup('TEST'), ())

    def test_single_nested_list_values_default(self):
        value = SingleNestedListValue()
        with env(DJANGO_TEST='2,3;4,5'):
            expected = [['2', '3'], ['4', '5']]
            self.assertEqual(value.setup('TEST'), expected)
        with env(DJANGO_TEST='2;3;4;5'):
            expected = [['2'], ['3'], ['4'], ['5']]
            self.assertEqual(value.setup('TEST'), expected)
        with env(DJANGO_TEST='2,3,4,5'):
            expected = [['2', '3', '4', '5']]
            self.assertEqual(value.setup('TEST'), expected)
        with env(DJANGO_TEST='2, 3 , ; 4 , 5 ; '):
            expected = [['2', '3'], ['4', '5']]
            self.assertEqual(value.setup('TEST'), expected)
        with env(DJANGO_TEST=''):
            self.assertEqual(value.setup('TEST'), [])

    def test_single_nested_list_values_separator(self):
        value = SingleNestedListValue(seq_separator=':')
        with env(DJANGO_TEST='2,3:4,5'):
            self.assertEqual(value.setup('TEST'), [['2', '3'], ['4', '5']])

    def test_single_nested_list_values_converter(self):
        value = SingleNestedListValue(converter=int)
        with env(DJANGO_TEST='2,3;4,5'):
            self.assertEqual(value.setup('TEST'), [[2, 3], [4, 5]])

    def test_single_nested_list_values_converter_default(self):
        value = SingleNestedListValue([['2', '3'], ['4', '5']], converter=int)
        self.assertEqual(value.value, [[2, 3], [4, 5]])

    def test_single_nested_tuple_values_default(self):
        value = SingleNestedTupleValue()
        with env(DJANGO_TEST='2,3;4,5'):
            expected = (('2', '3'), ('4', '5'))
            self.assertEqual(value.setup('TEST'), expected)
        with env(DJANGO_TEST='2;3;4;5'):
            expected = (('2',), ('3',), ('4',), ('5',))
            self.assertEqual(value.setup('TEST'), expected)
        with env(DJANGO_TEST='2,3,4,5'):
            expected = (('2', '3', '4', '5'),)
            self.assertEqual(value.setup('TEST'), expected)
        with env(DJANGO_TEST='2, 3 , ; 4 , 5 ; '):
            expected = (('2', '3'), ('4', '5'))
            self.assertEqual(value.setup('TEST'), expected)
        with env(DJANGO_TEST=''):
            self.assertEqual(value.setup('TEST'), ())

    def test_single_nested_tuple_values_separator(self):
        value = SingleNestedTupleValue(seq_separator=':')
        with env(DJANGO_TEST='2,3:4,5'):
            self.assertEqual(value.setup('TEST'), (('2', '3'), ('4', '5')))

    def test_single_nested_tuple_values_converter(self):
        value = SingleNestedTupleValue(converter=int)
        with env(DJANGO_TEST='2,3;4,5'):
            self.assertEqual(value.setup('TEST'), ((2, 3), (4, 5)))

    def test_single_nested_tuple_values_converter_default(self):
        value = SingleNestedTupleValue((('2', '3'), ('4', '5')), converter=int)
        self.assertEqual(value.value, ((2, 3), (4, 5)))

    def test_set_values_default(self):
        value = SetValue()
        with env(DJANGO_TEST='2,2'):
            self.assertEqual(value.setup('TEST'), {'2', '2'})
        with env(DJANGO_TEST='2, 2 ,'):
            self.assertEqual(value.setup('TEST'), {'2', '2'})
        with env(DJANGO_TEST=''):
            self.assertEqual(value.setup('TEST'), set())

    def test_dict_values_default(self):
        value = DictValue()
        with env(DJANGO_TEST='{2: 2}'):
            self.assertEqual(value.setup('TEST'), {2: 2})
        expected = {2: 2, '3': '3', '4': [1, 2, 3]}
        with env(DJANGO_TEST="{2: 2, '3': '3', '4': [1, 2, 3]}"):
            self.assertEqual(value.setup('TEST'), expected)
        with env(DJANGO_TEST="""{
                    2: 2,
                    '3': '3',
                    '4': [1, 2, 3],
                }"""):
            self.assertEqual(value.setup('TEST'), expected)
        with env(DJANGO_TEST=''):
            self.assertEqual(value.setup('TEST'), {})
        with env(DJANGO_TEST='spam'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_email_values(self):
        value = EmailValue('spam@eg.gs')
        with env(DJANGO_TEST='spam@sp.am'):
            self.assertEqual(value.setup('TEST'), 'spam@sp.am')
        with env(DJANGO_TEST='spam'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_url_values(self):
        value = URLValue('http://eggs.spam')
        with env(DJANGO_TEST='http://spam.eggs'):
            self.assertEqual(value.setup('TEST'), 'http://spam.eggs')
        with env(DJANGO_TEST='httb://spam.eggs'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_url_values_with_no_default(self):
        value = URLValue()  # no default
        with env(DJANGO_TEST='http://spam.eggs'):
            self.assertEqual(value.setup('TEST'), 'http://spam.eggs')

    def test_url_values_with_wrong_default(self):
        self.assertRaises(ValueError, URLValue, 'httb://spam.eggs')

    def test_ip_values(self):
        value = IPValue('0.0.0.0')
        with env(DJANGO_TEST='127.0.0.1'):
            self.assertEqual(value.setup('TEST'), '127.0.0.1')
        with env(DJANGO_TEST='::1'):
            self.assertEqual(value.setup('TEST'), '::1')
        with env(DJANGO_TEST='spam.eggs'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_regex_values(self):
        value = RegexValue('000--000', regex=r'\d+--\d+')
        with env(DJANGO_TEST='123--456'):
            self.assertEqual(value.setup('TEST'), '123--456')
        with env(DJANGO_TEST='123456'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_path_values_with_check(self):
        value = PathValue()
        with env(DJANGO_TEST='/'):
            self.assertEqual(value.setup('TEST'), '/')
        with env(DJANGO_TEST='~/'):
            self.assertEqual(value.setup('TEST'), os.path.expanduser('~'))
        with env(DJANGO_TEST='/does/not/exist'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_path_values_no_check(self):
        value = PathValue(check_exists=False)
        with env(DJANGO_TEST='/'):
            self.assertEqual(value.setup('TEST'), '/')
        with env(DJANGO_TEST='~/spam/eggs'):
            self.assertEqual(value.setup('TEST'),
                             os.path.join(os.path.expanduser('~'),
                                          'spam', 'eggs'))
        with env(DJANGO_TEST='/does/not/exist'):
            self.assertEqual(value.setup('TEST'), '/does/not/exist')

    def test_secret_value(self):
        # no default allowed, only environment values are
        self.assertRaises(ValueError, SecretValue, 'default')

        value = SecretValue()
        self.assertRaises(ValueError, value.setup, 'TEST')
        with env(DJANGO_SECRET_KEY='123'):
            self.assertEqual(value.setup('SECRET_KEY'), '123')

        value = SecretValue(environ_name='FACEBOOK_API_SECRET',
                            environ_prefix=None,
                            late_binding=True)
        self.assertRaises(ValueError, value.setup, 'TEST')
        with env(FACEBOOK_API_SECRET='123'):
            self.assertEqual(value.setup('TEST'), '123')

    def test_database_url_value(self):
        value = DatabaseURLValue()
        self.assertEqual(value.default, {})
        with env(DATABASE_URL='sqlite://'):
            self.assertEqual(value.setup('DATABASE_URL'), {
                'default': {
                    'CONN_MAX_AGE': 0,
                    'ENGINE': 'django.db.backends.sqlite3',
                    'HOST': '',
                    'NAME': ':memory:',
                    'PASSWORD': '',
                    'PORT': '',
                    'USER': '',
                }})

    def test_database_url_additional_args(self):

        def mock_database_url_caster(self, url, engine=None):
            return {'URL': url, 'ENGINE': engine}

        with patch('configurations.values.DatabaseURLValue.caster',
                   mock_database_url_caster):
            value = DatabaseURLValue(
                engine='django_mysqlpool.backends.mysqlpool')
            with env(DATABASE_URL='sqlite://'):
                self.assertEqual(value.setup('DATABASE_URL'), {
                    'default': {
                        'URL': 'sqlite://',
                        'ENGINE': 'django_mysqlpool.backends.mysqlpool'
                    }
                })

    def test_email_url_value(self):
        value = EmailURLValue()
        self.assertEqual(value.default, {})
        with env(EMAIL_URL='smtps://user@domain.com:password@smtp.example.com:587'):  # noqa: E501
            self.assertEqual(value.setup('EMAIL_URL'), {
                'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
                'EMAIL_FILE_PATH': '',
                'EMAIL_HOST': 'smtp.example.com',
                'EMAIL_HOST_PASSWORD': 'password',
                'EMAIL_HOST_USER': 'user@domain.com',
                'EMAIL_PORT': 587,
                'EMAIL_USE_SSL': False,
                'EMAIL_USE_TLS': True})
        with env(EMAIL_URL='console://'):
            self.assertEqual(value.setup('EMAIL_URL'), {
                'EMAIL_BACKEND': 'django.core.mail.backends.console.EmailBackend',  # noqa: E501
                'EMAIL_FILE_PATH': '',
                'EMAIL_HOST': None,
                'EMAIL_HOST_PASSWORD': None,
                'EMAIL_HOST_USER': None,
                'EMAIL_PORT': None,
                'EMAIL_USE_SSL': False,
                'EMAIL_USE_TLS': False})
        with env(EMAIL_URL='smtps://user@domain.com:password@smtp.example.com:wrong'):  # noqa: E501
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_cache_url_value(self):
        cache_setting = {
            'default': {
                'BACKEND': 'django_redis.cache.RedisCache',
                'LOCATION': 'redis://host:6379/1',
            }
        }
        cache_url = 'redis://user@host:6379/1'
        value = CacheURLValue(cache_url)
        self.assertEqual(value.default, cache_setting)
        value = CacheURLValue()
        self.assertEqual(value.default, {})
        with env(CACHE_URL='redis://user@host:6379/1'):
            self.assertEqual(value.setup('CACHE_URL'), cache_setting)
        with env(CACHE_URL='wrong://user@host:port/1'):
            with self.assertRaises(Exception) as cm:
                value.setup('TEST')
            self.assertEqual(cm.exception.args[0], 'Unknown backend: "wrong"')
        with env(CACHE_URL='redis://user@host:port/1'):
            with self.assertRaises(ValueError) as cm:
                value.setup('TEST')
            self.assertEqual(
                cm.exception.args[0],
                "Cannot interpret cache URL value 'redis://user@host:port/1'")

    def test_search_url_value(self):
        value = SearchURLValue()
        self.assertEqual(value.default, {})
        with env(SEARCH_URL='elasticsearch://127.0.0.1:9200/index'):
            self.assertEqual(value.setup('SEARCH_URL'), {
                'default': {
                    'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',  # noqa: E501
                    'URL': 'http://127.0.0.1:9200',
                    'INDEX_NAME': 'index',
                }})

    def test_backend_list_value(self):
        backends = ['django.middleware.common.CommonMiddleware']
        value = BackendsValue(backends)
        self.assertEqual(value.setup('TEST'), backends)

        backends = ['non.existing.Backend']
        self.assertRaises(ValueError, BackendsValue, backends)

    def test_tuple_value(self):
        value = TupleValue(None)
        self.assertEqual(value.default, ())
        self.assertEqual(value.value, ())

        value = TupleValue((1, 2))
        self.assertEqual(value.default, (1, 2))
        self.assertEqual(value.value, (1, 2))

    def test_set_value(self):
        value = SetValue()
        self.assertEqual(value.default, set())
        self.assertEqual(value.value, set())

        value = SetValue([1, 2])
        self.assertEqual(value.default, {1, 2})
        self.assertEqual(value.value, {1, 2})

    def test_setup_value(self):

        class Target:
            pass

        value = EmailURLValue()
        with env(EMAIL_URL='smtps://user@domain.com:password@smtp.example.com:587'):  # noqa: E501
            setup_value(Target, 'EMAIL', value)
            self.assertEqual(Target.EMAIL, {
                'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
                'EMAIL_FILE_PATH': '',
                'EMAIL_HOST': 'smtp.example.com',
                'EMAIL_HOST_PASSWORD': 'password',
                'EMAIL_HOST_USER': 'user@domain.com',
                'EMAIL_PORT': 587,
                'EMAIL_USE_SSL': False,
                'EMAIL_USE_TLS': True
            })
            self.assertEqual(
                Target.EMAIL_BACKEND,
                'django.core.mail.backends.smtp.EmailBackend')
            self.assertEqual(Target.EMAIL_FILE_PATH, '')
            self.assertEqual(Target.EMAIL_HOST, 'smtp.example.com')
            self.assertEqual(Target.EMAIL_HOST_PASSWORD, 'password')
            self.assertEqual(Target.EMAIL_HOST_USER, 'user@domain.com')
            self.assertEqual(Target.EMAIL_PORT, 587)
            self.assertEqual(Target.EMAIL_USE_TLS, True)
