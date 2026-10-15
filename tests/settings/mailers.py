from configurations import Configuration


class Parent(Configuration):
    SECRET_KEY = 'secret'

    MAILERS = {
        'default': {
            'BACKEND': 'django.core.mail.backends.console.EmailBackend',
        },
    }


class Child(Parent):
    pass
