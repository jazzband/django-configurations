import os
import subprocess
import sys

from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from unittest.mock import patch

from configurations.importer import ConfigurationFinder

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
TEST_PROJECT_DIR = os.path.join(ROOT_DIR, 'test_project')


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
        self.assertEqual(main.ALLOWED_HOSTS, ['base'])
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
        with self.assertRaises(ImproperlyConfigured):
            ConfigurationFinder()

    @patch.dict(os.environ, clear=True,
                DJANGO_SETTINGS_MODULE='tests.settings.main')
    def test_empty_class_var(self):
        with self.assertRaises(ImproperlyConfigured):
            ConfigurationFinder()

    def test_global_settings(self):
        from configurations.base import Configuration
        self.assertIn('dictConfig', Configuration.LOGGING_CONFIG)
        self.assertEqual(repr(Configuration),
                         "<Configuration 'configurations.base.Configuration'>")

    def test_deprecated_settings_but_set_by_user(self):
        from tests.settings.main import TestWithDefaultSetExplicitely
        TestWithDefaultSetExplicitely.setup()
        self.assertEqual(TestWithDefaultSetExplicitely.DEFAULT_AUTO_FIELD,
                         "django.db.models.BigAutoField")

    def test_repr(self):
        from tests.settings.main import Test
        self.assertEqual(repr(Test),
                         "<Configuration 'tests.settings.main.Test'>")

    @patch.dict(os.environ, clear=True,
                DJANGO_SETTINGS_MODULE='tests.settings.main',
                DJANGO_CONFIGURATION='Test')
    def test_initialization(self):
        finder = ConfigurationFinder()
        self.assertEqual(finder.module, 'tests.settings.main')
        self.assertEqual(finder.name, 'Test')
        self.assertEqual(
            repr(finder),
            "<ConfigurationFinder for 'tests.settings.main.Test'>")

    @patch.dict(os.environ, clear=True,
                DJANGO_SETTINGS_MODULE='tests.settings.inheritance',
                DJANGO_CONFIGURATION='Inheritance')
    def test_initialization_inheritance(self):
        finder = ConfigurationFinder()
        self.assertEqual(finder.module,
                         'tests.settings.inheritance')
        self.assertEqual(finder.name, 'Inheritance')

    @patch.dict(os.environ, clear=True,
                DJANGO_SETTINGS_MODULE='tests.settings.main',
                DJANGO_CONFIGURATION='NonExisting')
    @patch.object(sys, 'argv', ['python', 'manage.py', 'test',
                                '--settings=tests.settings.main',
                                '--configuration=Test'])
    def test_configuration_option(self):
        finder = ConfigurationFinder(check_options=False)
        self.assertEqual(finder.module, 'tests.settings.main')
        self.assertEqual(finder.name, 'NonExisting')
        finder = ConfigurationFinder(check_options=True)
        self.assertEqual(finder.module, 'tests.settings.main')
        self.assertEqual(finder.name, 'Test')

    def test_configuration_argument_in_cli(self):
        """
        Verify that's configuration option has been added to managements
        commands
        """
        proc = subprocess.Popen(['django-cadmin', 'test', '--help'],
                                stdout=subprocess.PIPE)
        self.assertIn('--configuration', proc.communicate()[0].decode('utf-8'))
        proc = subprocess.Popen(['django-cadmin', 'runserver', '--help'],
                                stdout=subprocess.PIPE)
        self.assertIn('--configuration', proc.communicate()[0].decode('utf-8'))

    def test_configuration_argument_in_runypy_cli(self):
        """
        Verify that's configuration option has been added to managements
        commands when using the -m entry point
        """
        proc = subprocess.Popen(
            [sys.executable, '-m', 'configurations', 'test', '--help'],
            stdout=subprocess.PIPE,
        )
        self.assertIn('--configuration', proc.communicate()[0].decode('utf-8'))
        proc = subprocess.Popen(
            [sys.executable, '-m', 'configurations', 'runserver', '--help'],
            stdout=subprocess.PIPE,
        )
        self.assertIn('--configuration', proc.communicate()[0].decode('utf-8'))

    def test_django_setup_only_called_once(self):
        proc = subprocess.Popen(
            [sys.executable, os.path.join(os.path.dirname(__file__),
                                          'setup_test.py')],
            stdout=subprocess.PIPE)
        res = proc.communicate()
        stdout = res[0].decode('utf-8')

        self.assertIn('setup_1', stdout)
        self.assertIn('setup_2', stdout)
        self.assertIn('setup_done', stdout)
        self.assertEqual(proc.returncode, 0)

    def test_utils_reraise(self):
        from configurations.utils import reraise

        class CustomException(Exception):
            pass

        with self.assertRaises(CustomException) as cm:
            try:
                raise CustomException
            except Exception as exc:
                reraise(exc, "Couldn't setup configuration", None)

        self.assertEqual(cm.exception.args, ("Couldn't setup configuration:   ",))
