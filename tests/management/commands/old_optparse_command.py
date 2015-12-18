from optparse import make_option
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    # Used by a specific test to see how unupgraded
    # management commands play with configurations.
    # See the test code for more details.

    option_list = BaseCommand.option_list + (
        make_option('--arg1', action='store_true'),
    )

    def handle(self, *args, **options):
        pass
