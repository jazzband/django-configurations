from . import importer

importer.install(check_options=True)

from django.core.management import (execute_from_command_line,  # noqa
                                    call_command)
