import os
import sys

from django.conf import global_settings
from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from mock import patch

from configurations.importer import ConfigurationImporter


class MainTests(TestCase):

    def test_simple(self):
        from tests.settings import main
        self.assertEqual(main.ATTRIBUTE_SETTING, True)
        self.assertEqual(main.PROPERTY_SETTING, 1)
        self.assertEqual(main.METHOD_SETTING, 2)
        self.assertEqual(main.LAMBDA_SETTING, 3)
        self.assertNotEqual(main.PRISTINE_LAMBDA_SETTING, 4)
        self.assertTrue(lambda: callable(main.PRISTINE_LAMBDA_SETTING))
        self.assertNotEqual(main.PRISTINE_FUNCTION_SETTING, 5)
        self.assertTrue(lambda: callable(main.PRISTINE_FUNCTION_SETTING))
        self.assertEqual(main.TEMPLATE_CONTEXT_PROCESSORS,
                         global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
                             'tests.settings.base.test_callback',
                         ))
        self.assertEqual(main.PRE_SETUP_TEST_SETTING, 6)
        self.assertRaises(AttributeError, lambda: main.POST_SETUP_TEST_SETTING)
        self.assertEqual(main.Test.POST_SETUP_TEST_SETTING, 7)

    def test_global_arrival(self):
        from django.conf import settings
        self.assertEqual(settings.PROPERTY_SETTING, 1)
        self.assertRaises(AttributeError, lambda: settings._PRIVATE_SETTING)
        self.assertNotEqual(settings.PRISTINE_LAMBDA_SETTING, 4)
        self.assertTrue(lambda: callable(settings.PRISTINE_LAMBDA_SETTING))
        self.assertNotEqual(settings.PRISTINE_FUNCTION_SETTING, 5)
        self.assertTrue(lambda: callable(settings.PRISTINE_FUNCTION_SETTING))
        self.assertEqual(settings.PRE_SETUP_TEST_SETTING, 6)

    @patch.dict(os.environ, clear=True, DJANGO_CONFIGURATION='Test')
    def test_empty_module_var(self):
        self.assertRaises(ImproperlyConfigured, ConfigurationImporter)

    @patch.dict(os.environ, clear=True,
                DJANGO_SETTINGS_MODULE='tests.settings.main')
    def test_empty_class_var(self):
        self.assertRaises(ImproperlyConfigured, ConfigurationImporter)

    def test_global_settings(self):
        from configurations.base import Configuration
        self.assertEqual(Configuration.LOGGING_CONFIG,
                         'django.utils.log.dictConfig')
        self.assertEqual(repr(Configuration),
                         "<Configuration 'configurations.base.Configuration'>")

    def test_repr(self):
        from tests.settings.main import Test
        self.assertEqual(repr(Test),
                         "<Configuration 'tests.settings.main.Test'>")

    @patch.dict(os.environ, clear=True,
                DJANGO_SETTINGS_MODULE='tests.settings.main',
                DJANGO_CONFIGURATION='Test')
    def test_initialization(self):
        importer = ConfigurationImporter()
        self.assertEqual(importer.module, 'tests.settings.main')
        self.assertEqual(importer.name, 'Test')
        self.assertEqual(repr(importer),
                         "<ConfigurationImporter for 'tests.settings.main.Test'>")

    @patch.dict(os.environ, clear=True,
                DJANGO_SETTINGS_MODULE='tests.settings.inheritance',
                DJANGO_CONFIGURATION='Inheritance')
    def test_initialization_inheritance(self):
        importer = ConfigurationImporter()
        self.assertEqual(importer.module,
                         'tests.settings.inheritance')
        self.assertEqual(importer.name, 'Inheritance')

    @patch.object(sys, 'argv', ['manage.py', 'test',
                  '--settings=tests.settings.main', '--configuration=Test'])
    def test_configuration_option(self):
        importer = ConfigurationImporter(check_options=True)
        self.assertEqual(importer.module, 'tests.settings.main')
        self.assertEqual(importer.name, 'Test')
        self.assertEqual(repr(importer),
                         "<ConfigurationImporter for 'tests.settings.main.Test'>")
