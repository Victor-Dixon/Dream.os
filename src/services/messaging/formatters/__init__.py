#!/usr/bin/env python3
"""
Formatters Package - Message Formatting Infrastructure
======================================================

<!-- SSOT Domain: messaging -->

Package containing specialized message formatters for different message categories.
Each formatter handles category-specific formatting rules and templates.

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

from .d2a_formatter import D2AFormatter
from .a2a_formatter import A2AFormatter
from .s2a_formatter import S2AFormatter
from .c2a_formatter import C2AFormatter
from .default_formatter import DefaultFormatter

__all__ = [
    'D2AFormatter',
    'A2AFormatter',
    'S2AFormatter',
    'C2AFormatter',
    'DefaultFormatter',
]