from configurations import Configuration, values


class DotEnvConfiguration(Configuration):

    DOTENV = {
        'path': 'some_nonexistant_path',
        'override': True,
        'required': False,
    }

    DOTENV_OVERRIDE = values.Value("Not overridden")
