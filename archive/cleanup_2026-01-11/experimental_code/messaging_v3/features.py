#!/usr/bin/env python3
"""
Advanced Features Integration - Pull in features from old system
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

from message import Message
from queue import MessageQueue
from delivery import send_message
from templates import MessageTemplates, get_template

logger = logging.getLogger(__name__)


class MessagingFeatures:
    """Integrate advanced features from the old messaging system."""

    def __init__(self):
        self.queue = MessageQueue()

    # ============================================================================
    # A2A (Agent-to-Agent) COORDINATION
    # ============================================================================

    def send_a2a_coordination(self, from_agent: str, to_agent: str, content: str,
                            coordination_type: str = "BILATERAL SWARM COORDINATION") -> bool:
        """Send A2A coordination message with proper formatting."""

        # Use the template system for consistent formatting
        formatted_content = get_template(
            "a2a_coordination",
            sender=from_agent,
            recipient=to_agent,
            content=content,
            coordination_type=coordination_type
        )

#A2A #{coordination_type.replace(' ', '-')} #SWARM-FORCE-MULTIPLIER
"""

        message = Message(
            id=None,
            sender=from_agent,
            recipient=to_agent,
            content=formatted_content,
            priority="regular",
            message_type="agent_to_agent",
            category="a2a"
        )

        msg_id = self.queue.enqueue(message)

        # Try immediate delivery
        if send_message(to_agent, formatted_content, from_agent):
            logger.info(f"✅ A2A coordination sent to {to_agent}")
            return True
        else:
            logger.warning(f"⚠️ A2A coordination queued for {to_agent} (ID: {msg_id})")
            return False

    # ============================================================================
    # BROADCAST MESSAGING
    # ============================================================================

    def broadcast_message(self, sender: str, content: str, priority: str = "urgent") -> int:
        """Broadcast message to all agents."""

        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-5",
                 "Agent-6", "Agent-7", "Agent-8"]
        # Note: Agent-4 is Captain, typically not included in broadcasts

        success_count = 0
        formatted_content = get_template("broadcast", sender=sender, content=content, priority=priority)

        for agent in agents:
            message = Message(
                id=None,
                sender=sender,
                recipient=agent,
                content=formatted_content,
                priority=priority,
                message_type="broadcast",
                category="broadcast"
            )

            self.queue.enqueue(message)

            if send_message(agent, formatted_content, sender):
                success_count += 1
                logger.info(f"✅ Broadcast delivered to {agent}")
            else:
                logger.warning(f"⚠️ Broadcast queued for {agent}")

        logger.info(f"📊 Broadcast sent to {len(agents)} agents, {success_count} immediate deliveries")
        return success_count

    # ============================================================================
    # ONBOARDING MESSAGES
    # ============================================================================

    def send_soft_onboarding(self, target_agent: str, sender: str = "SYSTEM") -> bool:
        """Send soft onboarding message."""

        content = get_template("soft_onboarding", sender=sender, recipient=target_agent)

        message = Message(
            id=None,
            sender=sender,
            recipient=target_agent,
            content=content,
            priority="regular",
            message_type="system_to_agent",
            category="s2a",
            metadata={"onboarding_type": "soft"}
        )

        msg_id = self.queue.enqueue(message)

        if send_message(target_agent, content, sender):
            logger.info(f"✅ Soft onboarding sent to {target_agent}")
            return True
        else:
            logger.warning(f"⚠️ Soft onboarding queued for {target_agent} (ID: {msg_id})")
            return False

    def send_hard_onboarding(self, target_agent: str, sender: str = "SYSTEM") -> bool:
        """Send hard onboarding message with full system context."""

        content = get_template("hard_onboarding", sender=sender, recipient=target_agent)

        message = Message(
            id=None,
            sender=sender,
            recipient=target_agent,
            content=content,
            priority="urgent",
            message_type="system_to_agent",
            category="s2a",
            metadata={"onboarding_type": "hard"}
        )

        msg_id = self.queue.enqueue(message)

        if send_message(target_agent, content, sender):
            logger.info(f"✅ Hard onboarding sent to {target_agent}")
            return True
        else:
            logger.warning(f"⚠️ Hard onboarding queued for {target_agent} (ID: {msg_id})")
            return False

    # ============================================================================
    # SURVEY COORDINATION
    # ============================================================================

    def coordinate_survey(self) -> bool:
        """Initiate survey coordination across all agents."""

        survey_content = get_template("survey_coordination", sender="SYSTEM")

        # Broadcast survey to all agents
        return self.broadcast_message("SYSTEM", survey_content, "high") > 0

    # ============================================================================
    # CONSOLIDATION COORDINATION
    # ============================================================================

    def coordinate_consolidation(self, batch_id: str, status: str) -> bool:
        """Coordinate consolidation across agents."""

        consolidation_content = get_template(
            "consolidation_coordination",
            sender="SYSTEM",
            batch_id=batch_id,
            consolidation_status=status
        )

        return self.broadcast_message("SYSTEM", consolidation_content, "urgent") > 0

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def get_queue_status(self) -> Dict[str, Any]:
        """Get comprehensive queue status."""
        count = self.queue.count()
        messages = self.queue.peek(10)

        status = {
            "total_messages": count,
            "messages": [
                {
                    "id": msg.id,
                    "sender": msg.sender,
                    "recipient": msg.recipient,
                    "priority": msg.priority,
                    "category": msg.category,
                    "created_at": msg.created_at.isoformat(),
                    "delivered": msg.delivered_at is not None
                } for msg in messages
            ]
        }

        return status

    def clear_old_messages(self, days: int = 7) -> int:
        """Clear messages older than specified days."""
        # This would need implementation in the queue class
        # For now, return 0
        logger.info(f"Clear old messages feature not yet implemented (would clear {days}+ day old messages)")
        return 0

    # ============================================================================
    # TASK MANAGEMENT INTEGRATION
    # ============================================================================

    def get_next_task(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get next task for agent (integration point for task system)."""
        try:
            # This would integrate with the task management system
            # For now, return a placeholder
            logger.info(f"Task system integration not yet implemented for {agent_id}")
            return None
        except Exception as e:
            logger.error(f"Failed to get next task for {agent_id}: {e}")
            return None

    def complete_task(self, task_id: str, agent_id: str) -> bool:
        """Mark task as completed (integration point for task system)."""
        try:
            # This would integrate with the task management system
            logger.info(f"Task completion integration not yet implemented: {task_id} by {agent_id}")
            return False
        except Exception as e:
            logger.error(f"Failed to complete task {task_id}: {e}")
            return False

    # ============================================================================
    # STATUS INTEGRATION
    # ============================================================================

    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get agent status from status.json integration."""
        try:
            # This would integrate with status.json system
            status_path = Path(f"agent_workspaces/Agent-{agent_id}/status.json")
            if status_path.exists():
                import json
                with open(status_path, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Failed to get status for {agent_id}: {e}")
            return None

    def update_agent_status(self, agent_id: str, updates: Dict[str, Any]) -> bool:
        """Update agent status in status.json."""
        try:
            status_path = Path(f"agent_workspaces/Agent-{agent_id}/status.json")
            current_status = {}

            if status_path.exists():
                import json
                with open(status_path, 'r') as f:
                    current_status = json.load(f)

            current_status.update(updates)
            current_status["last_updated"] = str(datetime.now())

            with open(status_path, 'w') as f:
                json.dump(current_status, f, indent=2)

            logger.info(f"Updated status for {agent_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to update status for {agent_id}: {e}")
            return False

    # ============================================================================
    # LEADERBOARD FUNCTIONALITY
    # ============================================================================

    def get_leaderboard(self) -> Dict[str, Any]:
        """Get agent performance leaderboard."""
        try:
            # This would aggregate performance metrics from all agents
            leaderboard = {
                "total_agents": 8,
                "active_agents": 0,
                "top_performers": [],
                "recent_activity": []
            }

            # Count active agents
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status = self.get_agent_status(agent_id)
                if status and status.get("status") == "ACTIVE_AGENT_MODE":
                    leaderboard["active_agents"] += 1

            logger.info("Leaderboard data compiled")
            return leaderboard
        except Exception as e:
            logger.error(f"Failed to get leaderboard: {e}")
            return {"error": str(e)}

    # ============================================================================
    # WORK RESUME GENERATION
    # ============================================================================

    def generate_work_resume(self, agent_id: str, include_recent_commits: bool = True,
                           include_coordination: bool = True, include_devlogs: bool = True) -> str:
        """
        Generate comprehensive work resume for agent.
        """
        try:
            resume_parts = [f"# Work Resume - {agent_id}", ""]

            # Agent status
            status = self.get_agent_status(agent_id)
            if status:
                resume_parts.append("## Current Status")
                resume_parts.append(f"- Status: {status.get('status', 'Unknown')}")
                resume_parts.append(f"- Current Mission: {status.get('current_mission', 'None')}")
                resume_parts.append(f"- Mission Priority: {status.get('mission_priority', 'Normal')}")
                resume_parts.append("")

            # Recent activity (would integrate with devlogs, commits, etc.)
            resume_parts.append("## Recent Activity")
            resume_parts.append("- Message coordination and delivery")
            resume_parts.append("- System integration and testing")
            resume_parts.append("- Swarm communication protocols")
            resume_parts.append("")

            # Skills and capabilities
            resume_parts.append("## Capabilities")
            resume_parts.append("- Cross-agent communication")
            resume_parts.append("- Coordination protocol execution")
            resume_parts.append("- Status reporting and updates")

            resume_parts.append('- Task management integration')
            resume_parts.append('')

            return '\\n'.join(resume_parts)

        except Exception as e:
            logger.error(f'Failed to generate work resume for {agent_id}: {e}')
            return f'# Work Resume - {agent_id}\\n\\nError generating resume: {e}'

    # ============================================================================
    # ROBINHOOD STATS (PLACEHOLDER)
    # ============================================================================

    def get_robinhood_stats(self) -> Dict[str, Any]:
        """
        Get Robinhood trading statistics (placeholder for integration).
        """
        try:
            # This would integrate with Robinhood API
            stats = {
                'total_trades': 0,
                'win_rate': 0.0,
                'total_pnl': 0.0,
                'active_positions': 0,
                'last_updated': str(datetime.now())
            }
            logger.info('Robinhood stats placeholder - integration not implemented')
            return stats
        except Exception as e:
            logger.error(f'Failed to get Robinhood stats: {e}')
            return {'error': str(e)}

