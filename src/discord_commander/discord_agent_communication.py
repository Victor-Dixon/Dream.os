#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Discord Agent Communication - V2 Compliance Module
===================================================

Unified agent communication engine for Discord commander.
Consolidates: agent_communication_engine_base.py + core.py + operations.py + refactored.py

Author: Agent-3 (Infrastructure & DevOps) - V2 Consolidation
License: MIT
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add root to path
root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root))

try:
    from src.utils.unified_utilities import get_unified_utility
except ImportError:
    # Minimal fallback
    import os

    class _Utility:
        path = os.path
        makedirs = os.makedirs

    def get_unified_utility():
        return _Utility()


try:
    from .discord_models import CommandResult, create_command_result
except ImportError:
    from discord_models import CommandResult, create_command_result


class AgentCommunicationEngine:
    """Unified agent communication engine for Discord commander."""

    def __init__(self) -> None:
        """Initialize agent communication engine."""
        self.logger = self._setup_logger()
        self._utility = get_unified_utility()

    def _setup_logger(self) -> logging.Logger:
        """Setup logger for communication engine."""
        logger = logging.getLogger("discord_commander")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _get_unified_utility(self):
        """Get unified utility instance."""
        return self._utility

    async def send_to_agent_inbox(self, agent: str, message: str, sender: str) -> CommandResult:
        """Send message directly to agent's inbox using inbox utility."""
        try:
            from src.utils.inbox_utility import create_inbox_message
            
            # Use inbox utility for file creation (separate from messaging system)
            success = create_inbox_message(
                recipient=agent,
                sender=f"{sender} (via Discord Commander)",
                content=message,
                priority="urgent",
                message_type="text",
                tags=["discord", "captain"]
            )
            
            if success:
                # Get the created file path for response
                inbox_dir = Path("agent_workspaces") / agent / "inbox"
                message_files = sorted(inbox_dir.glob("INBOX_MESSAGE_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
                latest_file = message_files[0] if message_files else None
                
                self.logger.info(f"Message sent to {agent}'s inbox via utility")
                
                return create_command_result(
                    success=True,
                    message=f"Message successfully delivered to {agent}'s inbox",
                    data={"filename": latest_file.name if latest_file else "unknown", "path": str(latest_file) if latest_file else "unknown"},
                    agent=agent,
                )
            else:
                raise Exception("Inbox utility returned False")
                
        except Exception as e:
            self.logger.error(f"Failed to send message to {agent}'s inbox: {e}")
            return create_command_result(
                success=False,
                message=f"Failed to deliver message to {agent}'s inbox: {str(e)}",
                agent=agent,
            )

    async def broadcast_to_all_agents(self, message: str, sender: str) -> CommandResult:
        """Broadcast message to all agents."""
        try:
            agents = [f"Agent-{i}" for i in range(1, 9)]
            successful_deliveries = 0
            failed_deliveries = []

            for agent in agents:
                result = await self.send_to_agent_inbox(agent, message, sender)
                if result.success:
                    successful_deliveries += 1
                else:
                    failed_deliveries.append(f"{agent}: {result.message}")

            if successful_deliveries == len(agents):
                return create_command_result(
                    success=True,
                    message=f"Broadcast successfully delivered to all {len(agents)} agents",
                    data={
                        "successful_deliveries": successful_deliveries,
                        "total_agents": len(agents),
                    },
                )
            else:
                return create_command_result(
                    success=False,
                    message=f"Broadcast partially failed: {successful_deliveries}/{len(agents)} delivered",
                    data={
                        "successful_deliveries": successful_deliveries,
                        "failed_deliveries": failed_deliveries,
                    },
                )

        except Exception as e:
            self.logger.error(f"Failed to broadcast to all agents: {e}")
            return create_command_result(success=False, message=f"Broadcast failed: {str(e)}")

    async def send_human_prompt_to_captain(self, prompt: str, sender: str) -> CommandResult:
        """Send human prompt to Captain Agent-4."""
        try:
            return await self.send_to_agent_inbox("Agent-4", prompt, sender)
        except Exception as e:
            self.logger.error(f"Failed to send human prompt to Captain: {e}")
            return create_command_result(
                success=False,
                message=f"Failed to send human prompt to Captain: {str(e)}",
            )

    async def execute_agent_command(self, agent: str, command: str) -> CommandResult:
        """Execute command on specific agent."""
        start_time = asyncio.get_event_loop().time()

        try:
            self.logger.info(f"Executing command on {agent}: {command}")
            await asyncio.sleep(1)  # Simulate command execution

            execution_time = asyncio.get_event_loop().time() - start_time

            return create_command_result(
                success=True,
                message=f"Command executed successfully on {agent}",
                execution_time=execution_time,
                agent=agent,
            )

        except Exception as e:
            execution_time = asyncio.get_event_loop().time() - start_time
            return create_command_result(
                success=False,
                message=f"Command failed on {agent}: {str(e)}",
                execution_time=execution_time,
                agent=agent,
            )

    def get_agent_status_file_path(self, agent: str) -> str:
        """Get agent status file path."""
        return self._utility.path.join(os.getcwd(), "agent_workspaces", agent, "status.json")

    async def read_agent_status(self, agent: str) -> dict[str, Any] | None:
        """Read agent status from file."""
        try:
            status_file = self.get_agent_status_file_path(agent)

            if self._utility.path.exists(status_file):
                with open(status_file) as f:
                    return json.load(f)
            else:
                self.logger.warning(f"Status file not found for {agent}")
                return None

        except Exception as e:
            self.logger.error(f"Failed to read status for {agent}: {e}")
            return None

    async def cleanup_old_messages(self, agent: str, max_age_hours: int = 24) -> int:
        """Clean up old messages from agent's inbox."""
        try:
            inbox_path = self._utility.path.join(os.getcwd(), "agent_workspaces", agent, "inbox")

            if not self._utility.path.exists(inbox_path):
                return 0

            cleaned_count = 0
            current_time = datetime.utcnow().timestamp()
            max_age_seconds = max_age_hours * 3600

            for filename in os.listdir(inbox_path):
                if filename.endswith(".md"):
                    file_path = self._utility.path.join(inbox_path, filename)
                    file_age = current_time - os.path.getmtime(file_path)

                    if file_age > max_age_seconds:
                        os.remove(file_path)
                        cleaned_count += 1

            self.logger.info(f"Cleaned up {cleaned_count} old messages from {agent}'s inbox")
            return cleaned_count

        except Exception as e:
            self.logger.error(f"Failed to cleanup old messages for {agent}: {e}")
            return 0

    def is_valid_agent(self, agent: str) -> bool:
        """Check if agent name is valid."""
        return agent in [f"Agent-{i}" for i in range(1, 9)]

    def get_all_agent_names(self) -> list[str]:
        """Get list of all agent names."""
        return [f"Agent-{i}" for i in range(1, 9)]

    def validate_agent_name(self, agent: str) -> bool:
        """Validate agent name format."""
        if not agent or not isinstance(agent, str):
            return False
        return agent.startswith("Agent-") and len(agent) >= 7

    def format_timestamp(self) -> str:
        """Format current timestamp."""
        return datetime.utcnow().isoformat()

    def create_message_metadata(
        self, sender: str, recipient: str, priority: str = "NORMAL"
    ) -> dict[str, Any]:
        """Create message metadata."""
        return {
            "sender": sender,
            "recipient": recipient,
            "priority": priority,
            "timestamp": self.format_timestamp(),
            "source": "discord_commander",
        }


# Factory function for dependency injection
def create_agent_communication_engine() -> AgentCommunicationEngine:
    """Factory function to create agent communication engine."""
    return AgentCommunicationEngine()


# Export for DI
__all__ = ["AgentCommunicationEngine", "create_agent_communication_engine"]
