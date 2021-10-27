import subprocess
import os

from django.test import TestCase
from django.conf import settings


class SphinxTests(TestCase):
    docs_dir = os.path.join(settings.BASE_DIR, 'docs')

    def test_multiprocessing(self):
        output = subprocess.check_output([
            'sphinx-build',
            '-b',
            'html',
            '-j 2',
            '.',
            '_build/html',
        ], cwd=self.docs_dir, stderr=subprocess.STDOUT)
        self.assertIn(b'build succeeded.', output)
