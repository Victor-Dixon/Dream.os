#!/usr/bin/env python3
"""
WP-CLI MCP Server - WordPress Command Line Interface
====================================================

<!-- SSOT Domain: web -->

MCP server providing WordPress CLI operations for automated WordPress management.
Supports plugin management, theme operations, database operations, and content management.

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

from .wp_cli_server import WPCliServer

__all__ = ['WPCliServer']