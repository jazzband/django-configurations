# -*- coding: utf-8 -*-
import subprocess
import os
from shutil import rmtree

from django.test import TestCase
from django.conf import settings
from django.utils.six import StringIO
from sphinx.application import Sphinx


class SphinxTests(TestCase):
    docs_dir = os.path.join(settings.BASE_DIR, 'docs')

    def tearDown(self):
        build_dir = os.path.join(self.docs_dir, '_build')
        if os.path.exists(build_dir):
            rmtree(build_dir)

    def test_extension(self):
        stdout = StringIO()
        s = Sphinx(
            self.docs_dir,
            self.docs_dir,
            '%s/_build/html' % self.docs_dir,
            '%s/_build/doctrees' % self.docs_dir,
            'html',
            status=stdout,
        )
        s.build()
        output = stdout.getvalue()
        stdout.close()
        self.assertIn('build succeeded.', output)

    def test_multiprocessing(self):
        output = subprocess.check_output([
            'sphinx-build',
            '-b',
            'html',
            '-j 2',
            '.',
            '_build/html',
        ], cwd=self.docs_dir, stderr=subprocess.STDOUT)
        self.assertIn(b'waiting for workers', output)
        self.assertIn(b'build succeeded.', output)
