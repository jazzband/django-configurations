import os

import django
from django.conf import Settings
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase

from unittest import skipUnless
from unittest.mock import patch


class MailersTests(TestCase):
    """
    Django 6.1 rejects the deprecated EMAIL_* settings alongside MAILERS, but the
    configuration class carries all of Django's global settings as defaults
    """

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='Parent',
                DJANGO_SETTINGS_MODULE='tests.settings.mailers')
    def test_mailers_omits_default_email_settings(self):
        from tests.settings import mailers
        self.assertEqual(
            mailers.MAILERS['default']['BACKEND'],
            'django.core.mail.backends.console.EmailBackend',
        )
        for name in ['EMAIL_BACKEND', 'EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_USE_TLS']:
            self.assertFalse(hasattr(mailers, name), name)

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='Parent',
                DJANGO_SETTINGS_MODULE='tests.settings.mailers')
    def test_mailers_keeps_other_email_settings(self):
        from tests.settings import mailers
        self.assertFalse(mailers.EMAIL_USE_LOCALTIME)

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='Parent',
                DJANGO_SETTINGS_MODULE='tests.settings.mailers')
    def test_mailers_loads_in_django(self):
        Settings('tests.settings.mailers')

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='Child',
                DJANGO_SETTINGS_MODULE='tests.settings.mailers')
    def test_mailers_inherited(self):
        from tests.settings import mailers
        self.assertIn('default', mailers.MAILERS)
        self.assertFalse(hasattr(mailers, 'EMAIL_BACKEND'))

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='Invalid',
                DJANGO_SETTINGS_MODULE='tests.settings.mailers_invalid')
    def test_mailers_with_email_setting_is_not_hidden(self):
        from tests.settings import mailers_invalid
        self.assertEqual(mailers_invalid.EMAIL_HOST, 'mail.example.com')
        self.assertFalse(hasattr(mailers_invalid, 'EMAIL_PORT'))

    @skipUnless(django.VERSION >= (6, 1), 'MAILERS requires Django 6.1')
    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='Invalid',
                DJANGO_SETTINGS_MODULE='tests.settings.mailers_invalid')
    def test_mailers_with_email_setting_is_rejected_by_django(self):
        from tests.settings import mailers_invalid  # noqa: F401
        with self.assertRaisesMessage(ImproperlyConfigured, 'EMAIL_HOST'):
            Settings('tests.settings.mailers_invalid')
