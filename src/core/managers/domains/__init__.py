"""
<!-- SSOT Domain: core -->

SSOT Domain Managers - Single Source of Truth for Core Domains
===============================================================

This module provides consolidated domain managers that replace multiple
specialized managers with unified SSOT implementations.

Available Domain Managers:
- ExecutionDomainManager: Consolidates execution and service coordination
- ResourceDomainManager: Consolidates resource operations (CRUD, file, lock)
- LifecycleDomainManager: Consolidates onboarding and recovery operations

V2 Compliance: Domain separation, single responsibility, consolidation benefits.

Owner: Agent-2 (Architecture & Design)
Last Updated: 2025-12-08
"""

from .execution_domain_manager import ExecutionDomainManager
from .resource_domain_manager import ResourceDomainManager
from .lifecycle_domain_manager import LifecycleDomainManager
from .results_domain_manager import ResultsDomainManager

__all__ = [
    "ExecutionDomainManager",
    "ResourceDomainManager",
    "LifecycleDomainManager",
    "ResultsDomainManager",
]
