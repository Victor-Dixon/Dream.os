# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

"""
SSOT TOOL METADATA
Purpose: Package marker for `tools.tests` to group toolbelt/unit smoke tests.
Description: Aggregates and exposes test modules for the `tools` package.
Usage:
  - python -m pytest tools/tests
  - python -m unittest discover -s tools/tests
Author: Swarm (maintainers)
Date: 2025-12-28
Tags: ssot, tests, python-package
"""

from . import test_adapters
from . import test_core
from . import test_registry
from . import test_smoke_categories

__all__ = [
    'test_adapters',
    'test_core',
    'test_registry',
    'test_smoke_categories',
]
