import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), os.pardir))

# setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.main")
os.environ.setdefault('DJANGO_CONFIGURATION', 'Test')

extensions = [
    'configurations.sphinx',
]

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'django-configurations'
copyright = '2012-2014, Jannis Leidel and other contributors'


version = release = 'test'

exclude_patterns = ['_build']

html_theme = 'default'
