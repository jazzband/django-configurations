import os
from django.test import TestCase
from unittest.mock import patch


class DotEnvLoadingTests(TestCase):

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='DotEnvConfiguration',
                DJANGO_SETTINGS_MODULE='tests.settings.dot_env')
    def test_env_loaded(self):
        from tests.settings import dot_env
        self.assertEqual(dot_env.DOTENV_VALUE, 'is set')
        self.assertEqual(dot_env.DOTENV_LOADED, dot_env.DOTENV)
