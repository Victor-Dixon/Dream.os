"""
<!-- SSOT Domain: messaging -->

Recovery Messaging - V2 Compliant
==================================

Message sending and notification helpers for recovery system.
Extracted from recovery.py for V2 compliance.

V2 Compliance: Focused module for recovery-related messaging.

Author: Agent-3 - Infrastructure & DevOps Specialist (extracted from Agent-1's work)
License: MIT
"""

import asyncio
import logging
import time

# V2 Integration imports
try:
    from ...core.messaging_pyautogui import send_message_to_agent
except ImportError:
    logging.warning("V2 messaging import failed, using mock")

    def send_message_to_agent(*args, **kwargs):
        logging.info(f"Mock message send: {args}, {kwargs}")
        return True


class RecoveryMessaging:
    """Handles all messaging/notification for recovery system."""

    def __init__(self, logger: logging.Logger):
        """Initialize recovery messaging."""
        self.logger = logger

    async def send_cycle_recovery_message(self, cycle_number: int, error_message: str) -> None:
        """Send recovery message for cycle failure to all active agents (mode-aware)."""
        try:
            self.logger.info(f"Sending cycle {cycle_number} recovery message")

            recovery_message = f"""
[RECOVERY] Cycle {cycle_number} Recovery
Error: {error_message}
Action: Continue with next cycle, report any issues.
Timestamp: {time.time()}
"""

            await self._broadcast_to_all_agents(recovery_message)
            self.logger.info("Cycle recovery messages sent")

        except Exception as e:
            self.logger.error(f"Failed to send cycle recovery messages: {e}")

    async def send_task_recovery_message(
        self, task_id: str, agent_id: str, error_message: str
    ) -> None:
        """Send recovery message for task failure to specific agent."""
        try:
            self.logger.info(f"Sending task recovery message to {agent_id}")

            recovery_message = f"""
[RECOVERY] Task {task_id} Recovery
Error: {error_message}
Action: Retry task or report if impossible.
Timestamp: {time.time()}
"""

            await asyncio.get_event_loop().run_in_executor(
                None, send_message_to_agent, agent_id, recovery_message
            )

            self.logger.info(f"Task recovery message sent to {agent_id}")

        except Exception as e:
            self.logger.error(f"Failed to send task recovery message: {e}")

    async def send_agent_rescue_message(self, agent_id: str, stall_duration_minutes: float = 0.0) -> None:
        """Send optimized rescue message to stalled agent with FSM and Cycle Planner integration."""
        try:
            self.logger.info(f"Sending optimized rescue message to {agent_id}")

            # Use optimized prompt generator
            from src.core.optimized_stall_resume_prompt import generate_optimized_resume_prompt
            
            rescue_message = generate_optimized_resume_prompt(
                agent_id=agent_id,
                fsm_state=None,  # Will be loaded from status.json
                last_mission=None,  # Will be loaded from status.json
                stall_duration_minutes=stall_duration_minutes
            )

            # Send via PyAutoGUI (primary method)
            await asyncio.get_event_loop().run_in_executor(
                None, send_message_to_agent, agent_id, rescue_message
            )

            # Also send Discord alert (enhancement - Agent-2 - 2025-01-27)
            try:
                from .monitor_discord_alerts import send_recovery_alert
                send_recovery_alert(agent_id, "attempted", "Rescue message sent via PyAutoGUI")
            except Exception as discord_error:
                self.logger.warning(f"Discord alert failed for {agent_id}: {discord_error}")

            self.logger.info(f"Rescue message sent to {agent_id}")

        except Exception as e:
            self.logger.error(f"Failed to send rescue message to {agent_id}: {e}")

    async def send_health_alert(self, issue: str, issue_id: str) -> None:
        """Send health alert to all active agents (mode-aware)."""
        try:
            self.logger.info(f"Sending health alert: {issue}")

            health_message = f"""
[HEALTH ALERT] System Issue Detected
Issue: {issue}
Action: Monitor and report status.
Issue ID: {issue_id}
Timestamp: {time.time()}
"""

            await self._broadcast_to_all_agents(health_message)
            self.logger.info("Health alerts sent")

        except Exception as e:
            self.logger.error(f"Failed to send health alerts: {e}")

    async def send_escalation_alert(
        self, escalation_id: str, failure_count: int, failure_summary: str
    ) -> None:
        """Send escalation alert to all active agents (mode-aware)."""
        try:
            self.logger.info(f"Sending escalation alert: {escalation_id}")

            escalation_message = f"""
[ESCALATION] Critical System Issues
Escalation ID: {escalation_id}
Recent Failures: {failure_count}
Summary: {failure_summary}
Action: Manual intervention required.
Timestamp: {time.time()}
"""

            await self._broadcast_to_all_agents(escalation_message)
            self.logger.info("Escalation alerts sent")

        except Exception as e:
            self.logger.error(f"Failed to send escalation alerts: {e}")

    async def _broadcast_to_all_agents(self, message: str) -> None:
        """Broadcast message to all active agents (mode-aware)."""
        try:
            from src.core.agent_mode_manager import get_active_agents
            active_agents = get_active_agents()
            self.logger.info(f"Mode-aware broadcast: Sending to {len(active_agents)} active agents: {', '.join(active_agents)}")
        except Exception as e:
            self.logger.warning(f"Failed to load mode-aware agents, using 4-agent fallback: {e}")
            # Fallback to 4-agent mode
            active_agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
        
        for agent_id in active_agents:
            try:
                await asyncio.get_event_loop().run_in_executor(
                    None, send_message_to_agent, agent_id, message
                )
            except Exception as e:
                self.logger.error(f"Failed to send message to {agent_id}: {e}")
