from configurations import Configuration, values


class DotEnvConfiguration(Configuration):

    DOTENV = 'test_project/.env'

    DOTENV_VALUE = values.Value()
