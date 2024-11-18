from configurations import Configuration


class ErrorConfiguration(Configuration):

    @classmethod
    def pre_setup(cls):
        raise ValueError("Error in pre_setup")
