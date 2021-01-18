import os

from django.test import TestCase

from unittest.mock import patch


class InheritanceTests(TestCase):

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='Inheritance',
                DJANGO_SETTINGS_MODULE='tests.settings.single_inheritance')
    def test_inherited(self):
        from tests.settings import single_inheritance
        self.assertEqual(
            single_inheritance.ALLOWED_HOSTS,
            ['test']
        )

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='Inheritance',
                DJANGO_SETTINGS_MODULE='tests.settings.multiple_inheritance')
    def test_inherited2(self):
        from tests.settings import multiple_inheritance
        self.assertEqual(
            multiple_inheritance.ALLOWED_HOSTS,
            ['test', 'test-test']
        )

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='Inheritance',
                DJANGO_SETTINGS_MODULE='tests.settings.mixin_inheritance')
    def test_inherited3(self):
        from tests.settings import mixin_inheritance
        self.assertEqual(
            mixin_inheritance.ALLOWED_HOSTS,
            ['test1', 'test2', 'test3']
        )
