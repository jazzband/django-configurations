import os
import importlib

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from unittest.mock import patch

from configurations import environ_prefix
from tests.settings import prefix_decorator


class EnvironPrefixDecoratorTests(TestCase):
    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION="PrefixDecoratorConf1",
                DJANGO_SETTINGS_MODULE="tests.settings.prefix_decorator",
                ACME_FOO="bar")
    def test_prefix_decorator_with_value(self):
        importlib.reload(prefix_decorator)
        self.assertEqual(prefix_decorator.FOO, "bar")

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION="PrefixDecoratorConf2",
                DJANGO_SETTINGS_MODULE="tests.settings.prefix_decorator",
                ACME_FOO="True")
    def test_prefix_decorator_for_value_subclasses(self):
        importlib.reload(prefix_decorator)
        self.assertIs(prefix_decorator.FOO, True)

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION="PrefixDecoratorConf3",
                DJANGO_SETTINGS_MODULE="tests.settings.prefix_decorator",
                ZEUS_FOO="bar")
    def test_value_prefix_takes_precedence(self):
        importlib.reload(prefix_decorator)
        self.assertEqual(prefix_decorator.FOO, "bar")

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION="PrefixDecoratorConf4",
                DJANGO_SETTINGS_MODULE="tests.settings.prefix_decorator",
                FOO="bar")
    def test_prefix_decorator_empty_string_value(self):
        importlib.reload(prefix_decorator)
        self.assertEqual(prefix_decorator.FOO, "bar")

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION="PrefixDecoratorConf5",
                DJANGO_SETTINGS_MODULE="tests.settings.prefix_decorator",
                FOO="bar")
    def test_prefix_decorator_none_value(self):
        importlib.reload(prefix_decorator)
        self.assertEqual(prefix_decorator.FOO, "bar")

    def test_prefix_value_must_be_none_or_str(self):
        class Conf:
            pass

        self.assertRaises(ImproperlyConfigured, lambda: environ_prefix(1)(Conf))
