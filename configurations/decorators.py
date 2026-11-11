from django.core.exceptions import ImproperlyConfigured


def pristinemethod(func):
    """
    A decorator for handling pristine settings like callables.

    Use it like this::

        from configurations import Configuration, pristinemethod

        class Develop(Configuration):

            @pristinemethod
            def USER_CHECK(user):
                return user.check_perms()

            GROUP_CHECK = pristinemethod(lambda user: user.has_group_access())

    """
    func.pristine = True
    return staticmethod(func)


def environ_prefix(prefix):
    """
    A class Configuration class decorator that prefixes ``prefix``
    to environment names.

    Use it like this::

        @environ_prefix("MYAPP")
        class Develop(Configuration):
            SOMETHING = values.Value()

    To remove the prefix from environment names::

        @environ_prefix(None)
        class Develop(Configuration):
            SOMETHING = values.Value()

    """
    if not isinstance(prefix, (type(None), str)):
        raise ImproperlyConfigured("environ_prefix accepts only str and None values.")

    def decorator(conf_cls):
        conf_cls._environ_prefix = prefix
        return conf_cls
    return decorator
