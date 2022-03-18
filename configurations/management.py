from . import importer
from .error_handling import with_error_handler

importer.install(check_options=True)

from django.core.management import (execute_from_command_line as dj_execute_from_command_line,  # noqa
                                    call_command as dj_call_command)

execute_from_command_line = with_error_handler(dj_execute_from_command_line)
call_command = with_error_handler(dj_call_command)
