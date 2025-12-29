#!/usr/bin/env python3
<!-- SSOT Domain: core -->
"""
Synthetic GitHub - Local-First GitHub Wrapper
=============================================

Thin wrapper that makes agents think they're talking to GitHub,
but routes 70% of calls to local storage, only 30% to real GitHub.

V2 Compliance: Adapter pattern, dependency inversion
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-11-28
Priority: CRITICAL - Bottleneck Breaking

NOTE: This file has been refactored into modules in src/core/github/
This file now serves as a compatibility shim for backward compatibility.
New code should import from src.core.github directly.
"""

# Backward compatibility imports
from .github import (
    SyntheticGitHub,
    GitHubSandboxMode,
    get_synthetic_github
)

__all__ = [
    "SyntheticGitHub",
    "GitHubSandboxMode",
    "get_synthetic_github",
]
