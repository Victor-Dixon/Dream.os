"""
Pytest Configuration for Messaging Templates Integration Tests
=============================================================

Disables plugin autoload to avoid dash/jupyter plugin overhead.
"""

import pytest


def pytest_configure(config):
    """Configure pytest for messaging templates integration tests."""
    # Disable plugins that cause overhead
    config.option.plugins = [
        p for p in config.option.plugins
        if p not in ['dash', 'jupyter', 'jupyter_client', 'ipykernel']
    ]



