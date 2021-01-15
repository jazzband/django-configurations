"""
invokes django-cadmin when the configurations module is run as a script.

Example: python -m configurations check
"""

from .management import execute_from_command_line

if __name__ == "__main__":
    execute_from_command_line()
