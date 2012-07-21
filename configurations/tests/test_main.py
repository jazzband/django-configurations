import os

from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured

from mock import patch

from ..importer import SettingsImporter


class MainTests(TestCase):

    def test_simple(self):
        from configurations.tests.settings import main
        self.assertEquals(main.LALA, 1)
        self.assertEquals(main.TEMPLATE_CONTEXT_PROCESSORS, (
            'django.contrib.auth.context_processors.auth',
            'django.core.context_processors.debug',
            'django.core.context_processors.i18n',
            'django.core.context_processors.media',
            'django.core.context_processors.static',
            'django.core.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            'configurations.tests.settings.base.test_callback',
        ))
        self.assertEquals(main.TEST_SETTING, True)

    def test_global_arrival(self):
        from django.conf import settings
        self.assertEquals(settings.LALA, 1)
        self.assertRaises(AttributeError, lambda: settings._SOMETHING)

    @patch.dict(os.environ, clear=True, DJANGO_CONFIGURATION='Test')
    def test_empty_module_var(self):
        self.assertRaises(ImproperlyConfigured, SettingsImporter)

    @patch.dict(os.environ, clear=True,
                DJANGO_SETTINGS_MODULE='configurations.tests.settings.main')
    def test_empty_class_var(self):
        self.assertRaises(ImproperlyConfigured, SettingsImporter)

    def test_global_settings(self):
        from configurations.base import Settings
        self.assertEquals(Settings.LOGGING_CONFIG, 'django.utils.log.dictConfig')
        self.assertEquals(repr(Settings),
                          "<Settings 'configurations.base.Settings'>")

    def test_repr(self):
        from configurations.tests.settings.main import Test
        self.assertEquals(repr(Test),
                          "<Settings 'configurations.tests.settings.main.Test'>")

    @patch.dict(os.environ, clear=True,
                DJANGO_SETTINGS_MODULE='configurations.tests.settings.main',
                DJANGO_CONFIGURATION='Test')
    def test_initialization(self):
        importer = SettingsImporter()
        self.assertEquals(importer.module, 'configurations.tests.settings.main')
        self.assertEquals(importer.name, 'Test')
        self.assertEquals(repr(importer),
                          "<SettingsImporter for 'configurations.tests.settings.main.Test'>")

    @patch.dict(os.environ, clear=True,
                DJANGO_SETTINGS_MODULE='configurations.tests.settings.inheritance',
                DJANGO_CONFIGURATION='Inheritance')
    def test_initialization_inheritance(self):
        importer = SettingsImporter()
        self.assertEquals(importer.module,
                          'configurations.tests.settings.inheritance')
        self.assertEquals(importer.name, 'Inheritance')
