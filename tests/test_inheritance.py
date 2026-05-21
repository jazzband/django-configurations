import os
import unittest

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

    @unittest.expectedFailure
    def test_mro_resolution(self):
        """
        A setting defined in Parent2 but not in Parent1 should be visible on
        Child(Parent1, Parent2) via standard MRO rather than being shadowed by
        the GrandParent value that the old attribute-copying code bakes into
        Parent1's class dict.
        """
        from tests.settings.mro_inheritance import Child
        self.assertEqual(Child.MY_SETTING, 'parent2')
