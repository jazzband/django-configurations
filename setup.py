from __future__ import print_function
import ast
import os
import codecs
from setuptools import setup


class VersionFinder(ast.NodeVisitor):
    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        if node.targets[0].id == '__version__':
            self.version = node.value.s


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def find_version(*parts):
    finder = VersionFinder()
    finder.visit(ast.parse(read(*parts)))
    return finder.version


setup(
    name="django-configurations",
    version=find_version("configurations", "__init__.py"),
    url='https://django-configurations.readthedocs.io/',
    license='BSD',
    description="A helper for organizing Django settings.",
    long_description=read('README.rst'),
    author='Jannis Leidel',
    author_email='jannis@leidel.info',
    packages=['configurations'],
    install_requires=['django'],
    entry_points={
        'console_scripts': [
            'django-cadmin = configurations.management:execute_from_command_line',
        ],
    },
    extras_require={
        'cache': ['django-cache-url'],
        'database': ['dj-database-url'],
        'email': ['dj-email-url'],
        'search': ['dj-search-url'],
        'testing': [
            'django-discover-runner',
            'mock',
            'django-cache-url>=1.0.0',
            'dj-database-url',
            'dj-email-url',
            'dj-search-url',
            'six',
            'Sphinx>=1.4',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    zip_safe=False,
)
