import os
from django.test import TestCase
from unittest.mock import patch


class ErrorTests(TestCase):

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='ErrorConfiguration',
                DJANGO_SETTINGS_MODULE='tests.settings.error')
    def test_env_loaded(self):
        with self.assertRaises(ValueError) as cm:
            from tests.settings import error  # noqa: F401

        self.assertIsInstance(cm.exception, ValueError)
        self.assertEqual(
            cm.exception.args,
            (
                "Couldn't setup configuration "
                "'tests.settings.error.ErrorConfiguration':  Error in pre_setup ",
            )
        )
