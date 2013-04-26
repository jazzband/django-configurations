import os
import uuid
from configurations import Settings


class Test(Settings):
    DEBUG = True

    SITE_ID = 1

    SECRET_KEY = str(uuid.uuid4())

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(os.path.dirname(__file__), 'test.db'),
        }
    }

    INSTALLED_APPS = [
        'django.contrib.sessions',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'django.contrib.auth',
        'django.contrib.admin',
        'configurations.tests',
    ]

    ROOT_URLCONF = 'configurations.tests.urls'

    TEST_RUNNER = 'discover_runner.DiscoverRunner'

    ATTRIBUTE_SETTING = True

    _PRIVATE_SETTING = 'ryan'

    @property
    def PROPERTY_SETTING(self):
        return 1

    def METHOD_SETTING(self):
        return 2

    LAMBDA_SETTING = lambda self: 3

    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return Settings.TEMPLATE_CONTEXT_PROCESSORS + (
            'configurations.tests.settings.base.test_callback',)
