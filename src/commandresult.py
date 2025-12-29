"""
Single Source of Truth (SSOT) for Command Execution Results
Domain: core
Owner: Agent-2 (Architecture & Design)
Last Updated: 2025-12-08
Related SSOT: src/swarmstatus.py, src/agent_registry.py

# SSOT Domain: core
"""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class CommandResult:
    """Represents the result of a command execution."""

    success: bool
    message: str
    data: Optional[Any] = None
    execution_time: Optional[float] = None
    agent: Optional[str] = None
