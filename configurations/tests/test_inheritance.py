import os

from django.test import TestCase

from mock import patch


class InheritanceTests(TestCase):

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='Inheritance',
                DJANGO_SETTINGS_MODULE='configurations.tests.settings.single_inheritance')
    def test_inherited(self):
        from configurations.tests.settings import single_inheritance
        self.assertEquals(single_inheritance.TEMPLATE_CONTEXT_PROCESSORS, (
            'django.contrib.auth.context_processors.auth',
            'django.core.context_processors.debug',
            'django.core.context_processors.i18n',
            'django.core.context_processors.media',
            'django.core.context_processors.static',
            'django.core.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            'configurations.tests.settings.base.test_callback',
        ))

    @patch.dict(os.environ, clear=True,
                DJANGO_CONFIGURATION='Inheritance',
                DJANGO_SETTINGS_MODULE='configurations.tests.settings.multiple_inheritance')
    def test_inherited2(self):
        from configurations.tests.settings import multiple_inheritance
        self.assertEquals(multiple_inheritance.TEMPLATE_CONTEXT_PROCESSORS, (
            'django.contrib.auth.context_processors.auth',
            'django.core.context_processors.debug',
            'django.core.context_processors.i18n',
            'django.core.context_processors.media',
            'django.core.context_processors.static',
            'django.core.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            'configurations.tests.settings.base.test_callback',
            'configurations.tests.settings.base.test_callback',
        ))
