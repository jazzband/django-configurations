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
