from configurations import Configuration


class Invalid(Configuration):
    SECRET_KEY = 'secret'

    MAILERS = {
        'default': {
            'BACKEND': 'django.core.mail.backends.console.EmailBackend',
        },
    }
    EMAIL_HOST = 'mail.example.com'
