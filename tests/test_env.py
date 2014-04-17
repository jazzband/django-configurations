import os
from django.test import TestCase
from configurations.values import BooleanValue
from mock import patch

class EnvValueTests(TestCase):

    def test_env_loaded(self):
        check_value = BooleanValue(False)
        self.assertEqual(check_value.setup('ENV_LOADED'), True)