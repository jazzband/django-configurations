def pristine(func):
    """
    A decorator for handling pristine settings like callables.

    Use it like this::

        from configurations import pristine

        class Develop(Settings):

            @pristine
            def USER_CHECK(user):
                return user.check_perms()

            GROUP_CHECK = pristine(lambda user: user.has_group_access())

    """
    func.pristine = True
    return staticmethod(func)
