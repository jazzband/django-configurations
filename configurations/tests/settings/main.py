import os
from configurations import Settings


class Test(Settings):
    SITE_ID = 1

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

    TEST_SETTING = True

    _SOMETHING = 'YEAH'

    DEBUG = True

    @property
    def LALA(self):
        return 1

    def LALA2(self):
        return 1

    def TEMPLATE_CONTEXT_PROCESSORS(self):
        return Settings.TEMPLATE_CONTEXT_PROCESSORS + (
            'configurations.tests.settings.base.test_callback',)
