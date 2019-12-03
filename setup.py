from __future__ import print_function
import os
import codecs
from setuptools import setup


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


setup(
    name="django-configurations",
    use_scm_version={"version_scheme": "post-release", "local_scheme": "dirty-tag"},
    setup_requires=["setuptools_scm"],
    url='https://django-configurations.readthedocs.io/',
    license='BSD',
    description="A helper for organizing Django settings.",
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
    author='Jannis Leidel',
    author_email='jannis@leidel.info',
    packages=['configurations'],
    entry_points={
        'console_scripts': [
            'django-cadmin = configurations.management:execute_from_command_line',
        ],
    },
    install_requires=['six'],
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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    zip_safe=False,
)
