import os

from django.conf import global_settings
from django.test import TestCase

from mock import patch


class InheritanceTests(TestCase):

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='Inheritance',
                DJANGO_SETTINGS_MODULE='configurations.tests.settings.single_inheritance')
    def test_inherited(self):
        from configurations.tests.settings import single_inheritance
        self.assertEquals(single_inheritance.TEMPLATE_CONTEXT_PROCESSORS,
                          global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
                              'configurations.tests.settings.base.test_callback',
                          ))

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='Inheritance',
                DJANGO_SETTINGS_MODULE='configurations.tests.settings.multiple_inheritance')
    def test_inherited2(self):
        from configurations.tests.settings import multiple_inheritance
        self.assertEquals(multiple_inheritance.TEMPLATE_CONTEXT_PROCESSORS,
                          global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
                              'configurations.tests.settings.base.test_callback',
                              'configurations.tests.settings.base.test_callback',
                          ))

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='MInheritance',
                DJANGO_SETTINGS_MODULE='configurations.tests.settings.multiple_inheritance2')
    def test_inherited3(self):
        from configurations.tests.settings import multiple_inheritance2
        self.assertEquals(multiple_inheritance2.TEMPLATE_CONTEXT_PROCESSORS,
                          global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
                              'configurations.tests.settings.base.test_callback3',
                              'configurations.tests.settings.base.test_callback2',
                              'configurations.tests.settings.base.test_callback1',
                              'configurations.tests.settings.base.test_callback_m',
                          ))
