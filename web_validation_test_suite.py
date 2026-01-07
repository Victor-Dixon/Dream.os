#!/usr/bin/env python3
"""
Web Validation Test Suite - Agent Cellphone V2
==============================================

SSOT Domain: web

Refactored entry point for web endpoint validation framework.
All core logic has been extracted into service architecture for V2 compliance.

Features:
- Parallel endpoint testing
- Health check validation
- Performance metrics collection
- Comprehensive reporting (web_validation_test_suite_v2.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

# Re-export the main classes and functions for backward compatibility
from web_validation_test_suite_v2 import (
    WebValidationTestSuite,
    main
)

# Re-export validation service for advanced usage
from src.web.validation_service import (
    WebValidationService,
    EndpointResult,
    ValidationReport,
    validation_service
)

__all__ = [
    "WebValidationTestSuite",
    "main",
    "WebValidationService",
    "EndpointResult",
    "ValidationReport",
    "validation_service"
]
