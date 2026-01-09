from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "Dream.OS"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "myst_parser",
    "sphinx_design",
    "sphinx_copybutton",
]

autosummary_generate = True
autodoc_typehints = "description"
napoleon_google_docstring = True
napoleon_numpy_docstring = False

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
]

html_theme = "alabaster"
