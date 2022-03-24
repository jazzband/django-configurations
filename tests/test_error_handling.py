import io
from unittest.mock import patch

from django.test import TestCase

from configurations.errors import ValueRetrievalError, SetupError, with_error_handler
from configurations.values import Value


class ErrorHandlingTestCase(TestCase):
    def test_help_text_in_explanation_lines(self):
        value_instance = Value(help_text="THIS IS A TEST")
        exception = ValueRetrievalError(value_instance)
        self.assertIn("Help: THIS IS A TEST", exception.explanation_lines)

    def test_help_reference_in_explanation_lines(self):
        value_instance = Value(help_reference="https://example.com")
        exception = ValueRetrievalError(value_instance)
        self.assertIn("Reference: https://example.com", exception.explanation_lines)

    def test_example_in_explanation_lines(self):
        value_instance = Value(example_generator=lambda: "test")
        exception = ValueRetrievalError(value_instance)
        self.assertIn("Example value: 'test'", exception.explanation_lines)

    def test_error_handler_rendering(self):
        # setup
        with patch("configurations.errors.sys.stderr", new=io.StringIO()) as mock:
            def inner():
                try:
                    value_instance = Value(environ_required=True)
                    value_instance.setup("TEST")
                except ValueRetrievalError as err:
                    raise SetupError("This is a test exception", [err])

            # execution
            with_error_handler(inner)()

            # verification
            self.assertEqual(mock.getvalue().strip(),
                             "This is a test exception\n"
                             "    * Value of TEST could not be retrieved from environment\n"
                             "        - TEST is taken from the environment variable DJANGO_TEST as a Value")
