from configurations import Configuration, values


class DotEnvConfiguration(Configuration):

    DOTENV = {
        'path': 'test_project/.env',
        'override': True,
    }

    DOTENV_VALUE = values.Value()
    DOTENV_OVERRIDE = values.Value("Not overridden")
