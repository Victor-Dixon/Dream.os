"""
Agent Cellphone V2 - Multi-Agent Coordination System
====================================================

A professional multi-agent coordination system for automated task management,
real-time collaboration, and intelligent workflow orchestration.

Features:
- Multi-agent coordination with swarm intelligence
- Real-time collaborative editing with OT/CRDT
- AI-powered UX and predictive analytics
- Professional API with FastAPI
- Discord integration for agent communication

Example:
    >>> from agent_cellphone_v2 import AgentCoordinator
    >>> coordinator = AgentCoordinator()
    >>> coordinator.start()
"""

__version__ = "2.0.0"
__author__ = "DadudeCK"
__email__ = "dadudekc@gmail.com"

from .core import AgentCoordinator

__all__ = ["AgentCoordinator"]