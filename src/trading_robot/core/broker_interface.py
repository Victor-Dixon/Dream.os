"""
Trading Robot Broker Interface
==============================

SSOT Domain: trading_robot

V2 Compliant: <50 lines, single responsibility
Re-export of BrokerInterface for consistent imports.

Author: Agent-2 (dream.os)
Date: 2026-01-08
"""

# Re-export BrokerInterface from broker_factory for consistent imports
from .broker_factory import BrokerInterface

__all__ = ["BrokerInterface"]