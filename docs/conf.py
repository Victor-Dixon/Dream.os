# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Agent Cellphone V2'
copyright = '2026, Swarm Intelligence Collective'
author = 'Agent-7 (Documentation & CLI Enhancement Lead)'
release = '2.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',      # Core autodoc functionality
    'sphinx.ext.autosummary',  # Generate autosummary tables
    'sphinx.ext.viewcode',     # Add source code links
    'sphinx.ext.napoleon',     # Support for NumPy/Google style docstrings
    'sphinx.ext.intersphinx',  # Link to external documentation
    'sphinx.ext.todo',         # Support for TODO directives
    'sphinx.ext.coverage',     # Check documentation coverage
    'sphinx.ext.doctest',      # Test code in docstrings
    'sphinx.ext.githubpages',  # GitHub Pages support
]

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
    'member-order': 'bysource',
    'special-members': '__init__',
}

# Autosummary settings
autosummary_generate = True
autosummary_imported_members = True

# Napoleon settings (Google/NumPy docstring support)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'discord': ('https://discordpy.readthedocs.io/en/stable/', None),
    'requests': ('https://requests.readthedocs.io/en/latest/', None),
}

# Doctest settings
doctest_global_setup = '''
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
'''

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Theme options
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    # Toc options
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# Custom CSS
html_css_files = [
    'css/custom.css',
]

# Logo and favicon
html_logo = '_static/logo.png'
html_favicon = '_static/favicon.ico'

# -- Options for manual page output ------------------------------------------
man_pages = [
    ('index', 'agentcellphonev2', 'Agent Cellphone V2 Documentation', [author], 1)
]

# -- Extension configuration --------------------------------------------------

# Todo extension
todo_include_todos = True

# Coverage extension
coverage_modules = [
    'src.core.messaging_core',
    'src.services.messaging_cli',
    'src.discord_commander.base',
]

# Viewcode extension
viewcode_import = True