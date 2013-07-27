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
        self.assertEqual(single_inheritance.TEMPLATE_CONTEXT_PROCESSORS,
                          global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
                              'configurations.tests.settings.base.test_callback',
                          ))

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='Inheritance',
                DJANGO_SETTINGS_MODULE='configurations.tests.settings.multiple_inheritance')
    def test_inherited2(self):
        from configurations.tests.settings import multiple_inheritance
        self.assertEqual(multiple_inheritance.TEMPLATE_CONTEXT_PROCESSORS,
                          global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
                              'configurations.tests.settings.base.test_callback',
                              'configurations.tests.settings.base.test_callback',
                          ))

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='Inheritance',
                DJANGO_SETTINGS_MODULE='configurations.tests.settings.mixin_inheritance')
    def test_inherited3(self):
        from configurations.tests.settings import mixin_inheritance
        self.assertEqual(mixin_inheritance.TEMPLATE_CONTEXT_PROCESSORS,
                          global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
                              'some_app.context_processors.processor1',
                              'some_app.context_processors.processor2',
                              'some_app.context_processors.processorbase',
                          ))
