from configurations import Configuration, values


class DotEnvConfiguration(Configuration):

    DOTENV = 'test_project/.env'

    DOTENV_VALUE = values.Value()

    def DOTENV_VALUE_METHOD(self):
        return values.Value(environ_name="DOTENV_VALUE")
