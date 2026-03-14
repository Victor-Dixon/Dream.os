#!/usr/bin/env python3
# Header-Variant: full
# Owner: Dream.os
# Purpose: Module implementation and orchestration logic.
# SSOT: docs/recovery/recovery_registry.yaml#src-core-messaging-init
# @registry docs/recovery/recovery_registry.yaml#src-core-messaging-init

"""
Messaging Protocol - SSOT for Messaging Interfaces
==================================================

Provides single source of truth for messaging protocol interfaces.
Consolidates messaging method signatures across implementations.

<!-- SSOT Domain: core -->

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
"""

# Re-export the protocol from stress_testing for central access
from ..stress_testing.messaging_core_protocol import MessagingCoreProtocol

__all__ = ["MessagingCoreProtocol"]


