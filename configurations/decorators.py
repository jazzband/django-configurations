def pristinemethod(func):
    """
    A decorator for handling pristine settings like callables.

    Use it like this::

        from configurations import pristinemethod

        class Develop(Settings):

            @pristinemethod
            def USER_CHECK(user):
                return user.check_perms()

            GROUP_CHECK = pristinemethod(lambda user: user.has_group_access())

    """
    func.pristine = True
    return staticmethod(func)
