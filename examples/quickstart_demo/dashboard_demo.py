from __future__ import annotations

import logging
logger = logging.getLogger(__name__)
"""Text-based dashboard demo for AutoDream OS.

Shows how agent status might be displayed."""
from enum import Enum


# NOTE: This is a demo-only enum. For production code, use:
# from src.core.intelligent_context.enums import AgentStatus
class DemoAgentStatus(Enum):
    """Demo-only agent status enum (not for production use)."""
    ONLINE = 'online'
    IDLE = 'idle'
    OFFLINE = 'offline'


def get_agent_status() ->dict[str, DemoAgentStatus]:
    """Return a mapping of agent names to their statuses (demo only)."""
    return {'Agent-1': DemoAgentStatus.ONLINE, 'Agent-2': DemoAgentStatus.IDLE,
        'Agent-3': DemoAgentStatus.OFFLINE}


def display_dashboard() ->None:
    """Display a simple dashboard of agent statuses."""
    status = get_agent_status()
    logger.info('Agent Status Dashboard')
    for name, state in status.items():
        logger.info(f'{name}: {state.value}')


if __name__ == '__main__':
    display_dashboard()
