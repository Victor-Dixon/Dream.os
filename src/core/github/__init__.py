#!/usr/bin/env python3
"""
GitHub Module - Synthetic GitHub Package
========================================

<!-- SSOT Domain: integration -->

Public API exports for synthetic GitHub wrapper.
Extracted from synthetic_github.py for V2 compliance.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

from typing import Optional

from .synthetic_client import SyntheticGitHub
from .sandbox_manager import GitHubSandboxMode

# Global instance
_synthetic_github: Optional[SyntheticGitHub] = None


def get_synthetic_github() -> SyntheticGitHub:
    """Get global SyntheticGitHub instance."""
    global _synthetic_github
    if _synthetic_github is None:
        _synthetic_github = SyntheticGitHub()
    return _synthetic_github


__all__ = [
    "SyntheticGitHub",
    "GitHubSandboxMode",
    "get_synthetic_github",
]



