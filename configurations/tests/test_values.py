import decimal
import os
from contextlib import contextmanager

from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from mock import patch

from configurations.values import (Value, BooleanValue, IntegerValue,
                                   FloatValue, DecimalValue, ListValue,
                                   TupleValue, SetValue, DictValue,
                                   URLValue, EmailValue, IPValue,
                                   RegexValue, PathValue, SecretValue,
                                   DatabaseURLValue, EmailURLValue,
                                   CacheURLValue, BackendsValue,
                                   CastingMixin)


@contextmanager
def env(**kwargs):
    with patch.dict(os.environ, clear=True, **kwargs):
        yield


class FailingCasterValue(CastingMixin, Value):
    caster = 'non.existing.caster'


class ValueTests(TestCase):

    def test_value(self):
        value = Value('default')
        self.assertEqual(value.setup('TEST'), 'default')
        with env(DJANGO_TEST='override'):
            self.assertEqual(value.setup('TEST'), 'default')

    @patch.dict(os.environ, clear=True, DJANGO_TEST='override')
    def test_env_var(self):
        value = Value('default', environ=True)
        self.assertEqual(value.setup('TEST'), 'override')
        self.assertNotEqual(value.setup('TEST'), value.default)
        self.assertEqual(value.to_python(os.environ['DJANGO_TEST']),
                         value.setup('TEST'))

    def test_value_reuse(self):
        value1 = Value('default', environ=True)
        value2 = Value(value1, environ=True)
        self.assertEqual(value1.setup('TEST1'), 'default')
        self.assertEqual(value2.setup('TEST2'), 'default')
        with env(DJANGO_TEST1='override1', DJANGO_TEST2='override2'):
            self.assertEqual(value1.setup('TEST1'), 'override1')
            self.assertEqual(value2.setup('TEST2'), 'override2')

    def test_env_var_prefix(self):
        with patch.dict(os.environ, clear=True, ACME_TEST='override'):
            value = Value('default', environ=True, environ_prefix='ACME')
            self.assertEqual(value.setup('TEST'), 'override')

        with patch.dict(os.environ, clear=True, TEST='override'):
            value = Value('default', environ=True, environ_prefix='')
            self.assertEqual(value.setup('TEST'), 'override')

    def test_boolean_values_true(self):
        value = BooleanValue(False, environ=True)
        for truthy in value.true_values:
            with env(DJANGO_TEST=truthy):
                self.assertTrue(value.setup('TEST'))

    def test_boolean_values_faulty(self):
        self.assertRaises(ValueError, BooleanValue, 'false')

    def test_boolean_values_false(self):
        value = BooleanValue(True, environ=True)
        for falsy in value.false_values:
            with env(DJANGO_TEST=falsy):
                self.assertFalse(value.setup('TEST'))

    def test_boolean_values_nonboolean(self):
        value = BooleanValue(True, environ=True)
        with env(DJANGO_TEST='nonboolean'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_integer_values(self):
        value = IntegerValue(1, environ=True)
        with env(DJANGO_TEST='2'):
            self.assertEqual(value.setup('TEST'), 2)
        with env(DJANGO_TEST='noninteger'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_float_values(self):
        value = FloatValue(1.0, environ=True)
        with env(DJANGO_TEST='2.0'):
            self.assertEqual(value.setup('TEST'), 2.0)
        with env(DJANGO_TEST='noninteger'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_decimal_values(self):
        value = DecimalValue(decimal.Decimal(1), environ=True)
        with env(DJANGO_TEST='2'):
            self.assertEqual(value.setup('TEST'), decimal.Decimal(2))
        with env(DJANGO_TEST='nondecimal'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_failing_caster(self):
        self.assertRaises(ImproperlyConfigured, FailingCasterValue)

    def test_list_values_default(self):
        value = ListValue(environ=True)
        with env(DJANGO_TEST='2,2'):
            self.assertEqual(value.setup('TEST'), ['2', '2'])
        with env(DJANGO_TEST='2, 2 ,'):
            self.assertEqual(value.setup('TEST'), ['2', '2'])
        with env(DJANGO_TEST=''):
            self.assertEqual(value.setup('TEST'), [])

    def test_list_values_separator(self):
        value = ListValue(environ=True, separator=':')
        with env(DJANGO_TEST='/usr/bin:/usr/sbin:/usr/local/bin'):
            self.assertEqual(value.setup('TEST'),
                             ['/usr/bin', '/usr/sbin', '/usr/local/bin'])

    def test_List_values_converter(self):
        value = ListValue(environ=True, converter=int)
        with env(DJANGO_TEST='2,2'):
            self.assertEqual(value.setup('TEST'), [2, 2])

        value = ListValue(environ=True, converter=float)
        with env(DJANGO_TEST='2,2'):
            self.assertEqual(value.setup('TEST'), [2.0, 2.0])

    def test_list_values_custom_converter(self):
        value = ListValue(environ=True, converter=lambda x: x * 2)
        with env(DJANGO_TEST='2,2'):
            self.assertEqual(value.setup('TEST'), ['22', '22'])

    def test_list_values_converter_exception(self):
        value = ListValue(environ=True, converter=int)
        with env(DJANGO_TEST='2,b'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_tuple_values_default(self):
        value = TupleValue(environ=True)
        with env(DJANGO_TEST='2,2'):
            self.assertEqual(value.setup('TEST'), ('2', '2'))
        with env(DJANGO_TEST='2, 2 ,'):
            self.assertEqual(value.setup('TEST'), ('2', '2'))
        with env(DJANGO_TEST=''):
            self.assertEqual(value.setup('TEST'), ())

    def test_set_values_default(self):
        value = SetValue(environ=True)
        with env(DJANGO_TEST='2,2'):
            self.assertEqual(value.setup('TEST'), set(['2', '2']))
        with env(DJANGO_TEST='2, 2 ,'):
            self.assertEqual(value.setup('TEST'), set(['2', '2']))
        with env(DJANGO_TEST=''):
            self.assertEqual(value.setup('TEST'), set())

    def test_dict_values_default(self):
        value = DictValue(environ=True)
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
        value = EmailValue('spam@eg.gs', environ=True)
        with env(DJANGO_TEST='spam@sp.am'):
            self.assertEqual(value.setup('TEST'), 'spam@sp.am')
        with env(DJANGO_TEST='spam'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_url_values(self):
        value = URLValue('http://eggs.spam', environ=True)
        with env(DJANGO_TEST='http://spam.eggs'):
            self.assertEqual(value.setup('TEST'), 'http://spam.eggs')
        with env(DJANGO_TEST='httb://spam.eggs'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_ip_values(self):
        value = IPValue('0.0.0.0', environ=True)
        with env(DJANGO_TEST='127.0.0.1'):
            self.assertEqual(value.setup('TEST'), '127.0.0.1')
        with env(DJANGO_TEST='::1'):
            self.assertEqual(value.setup('TEST'), '::1')
        with env(DJANGO_TEST='spam.eggs'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_regex_values(self):
        value = RegexValue('000--000', environ=True, regex=r'\d+--\d+')
        with env(DJANGO_TEST='123--456'):
            self.assertEqual(value.setup('TEST'), '123--456')
        with env(DJANGO_TEST='123456'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_path_values_with_check(self):
        value = PathValue(environ=True)
        with env(DJANGO_TEST='/'):
            self.assertEqual(value.setup('TEST'), '/')
        with env(DJANGO_TEST='~/'):
            self.assertEqual(value.setup('TEST'), os.path.expanduser('~'))
        with env(DJANGO_TEST='/does/not/exist'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_path_values_no_check(self):
        value = PathValue(environ=True, check_exists=False)
        with env(DJANGO_TEST='/'):
            self.assertEqual(value.setup('TEST'), '/')
        with env(DJANGO_TEST='~/spam/eggs'):
            self.assertEqual(value.setup('TEST'),
                             os.path.join(os.path.expanduser('~'),
                                          'spam', 'eggs'))
        with env(DJANGO_TEST='/does/not/exist'):
            self.assertEqual(value.setup('TEST'), '/does/not/exist')

    def test_secret_value(self):
        self.assertRaises(ValueError, SecretValue, 'default')
        value = SecretValue()
        self.assertRaises(ValueError, value.setup, 'TEST')
        with env(DJANGO_SECRET_KEY='123'):
            self.assertEqual(value.setup('SECRET_KEY'), '123')

    def test_database_url_value(self):
        value = DatabaseURLValue(environ=True)
        self.assertEqual(value.default, {})
        with env(DATABASE_URL='sqlite://'):
            self.assertEqual(value.setup('DATABASE_URL'), {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'HOST': None,
                    'NAME': ':memory:',
                    'PASSWORD': None,
                    'PORT': None,
                    'USER': None,
                }})

    def test_email_url_value(self):
        value = EmailURLValue(environ=True)
        self.assertEqual(value.default, {})
        with env(EMAIL_URL='smtps://user@domain.com:password@smtp.example.com:587'):
            self.assertEqual(value.setup('EMAIL_URL'), {
                'EMAIL_BACKEND': 'django.core.mail.backends.smtp.EmailBackend',
                'EMAIL_FILE_PATH': '',
                'EMAIL_HOST': 'smtp.example.com',
                'EMAIL_HOST_PASSWORD': 'password',
                'EMAIL_HOST_USER': 'user@domain.com',
                'EMAIL_PORT': 587,
                'EMAIL_USE_TLS': True})
        with env(EMAIL_URL='console://'):
            self.assertEqual(value.setup('EMAIL_URL'), {
                'EMAIL_BACKEND': 'django.core.mail.backends.console.EmailBackend',
                'EMAIL_FILE_PATH': '',
                'EMAIL_HOST': None,
                'EMAIL_HOST_PASSWORD': None,
                'EMAIL_HOST_USER': None,
                'EMAIL_PORT': None,
                'EMAIL_USE_TLS': False})
        with env(EMAIL_URL='smtps://user@domain.com:password@smtp.example.com:wrong'):
            self.assertRaises(ValueError, value.setup, 'TEST')

    def test_cache_url_value(self):
        value = CacheURLValue(environ=True)
        self.assertEqual(value.default, {})
        with env(CACHE_URL='redis://user@host:port/1'):
            self.assertEqual(value.setup('CACHE_URL'), {
                'default': {
                    'BACKEND': 'redis_cache.cache.RedisCache',
                    'KEY_PREFIX': '',
                    'LOCATION': 'user@host:port:1'
                }})
        with env(CACHE_URL='wrong://user@host:port/1'):
            self.assertRaises(KeyError, value.setup, 'TEST')

    def test_backend_list_value(self):
        backends = ['django.middleware.common.CommonMiddleware']
        value = BackendsValue(backends)
        self.assertEqual(value.setup('TEST'), backends)

        backends = ['non.existing.Backend']
        self.assertRaises(ImproperlyConfigured, BackendsValue, backends)
