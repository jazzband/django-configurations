import configurations

# -- Project information -----------------------------------------------------
project = 'django-configurations'
copyright = '2012-2021, Jannis Leidel and other contributors'
author = 'Jannis Leidel and other contributors'

release = configurations.__version__
version = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------
add_function_parentheses = False
add_module_names = False

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master', None),
    'django': ('https://docs.djangoproject.com/en/dev',
               'https://docs.djangoproject.com/en/dev/_objects/'),
}

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'

# -- Options for Epub output ---------------------------------------------------
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

# -- Options for LaTeX output --------------------------------------------------
latex_documents = [
    # (source start file, target name, title, author, documentclass)
    ('index', 'django-configurations.tex',
     'django-configurations Documentation', author, 'manual'),
]
