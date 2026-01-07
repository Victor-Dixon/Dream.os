#!/usr/bin/env python3
"""
Setup Wizard - Agent Cellphone V2
=================================

SSOT Domain: core

Refactored entry point for interactive setup wizard.
All core logic has been extracted into service architecture for V2 compliance.

Features:
- Interactive configuration
- Environment validation
- Service setup
- Configuration management (setup_wizard_v2.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

# Re-export the main classes and functions for backward compatibility
from setup_wizard_v2 import (
    SetupWizard,
    main
