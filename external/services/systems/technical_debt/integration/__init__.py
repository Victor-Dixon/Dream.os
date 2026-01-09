"""
Technical Debt System Integration Module
========================================

Integrates technical debt tracking with:
- Agent Status Monitor (task assignment)
- Master Task Log (task visibility)
- Audit Trail (compliance tracking)

<!-- SSOT Domain: integration -->
"""

from .agent_status_integration import AgentStatusDebtIntegration
from .master_task_integration import MasterTaskDebtIntegration
from .audit_integration import AuditDebtIntegration

__all__ = [
    "AgentStatusDebtIntegration",
    "MasterTaskDebtIntegration",
    "AuditDebtIntegration",
]