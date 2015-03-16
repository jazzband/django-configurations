#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings.main'
    os.environ['DJANGO_CONFIGURATION'] = 'Test'

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
