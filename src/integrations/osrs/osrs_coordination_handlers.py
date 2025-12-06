"""
OSRS Coordination Handlers - V2 Compliant
==========================================

<!-- SSOT Domain: communication -->

Message handling and coordination logic for OSRS agents.
Extracted from osrs_agent_core.py for V2 compliance.

Author: Agent-6 - Coordination & Communication Specialist
Date: 2025-12-03
"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .osrs_agent_core import OSRS_Agent_Core


class OSRSCoordinationHandlers:
    """Handles coordination messages between OSRS agents."""

    def __init__(self, agent: "OSRS_Agent_Core"):
        """Initialize with agent reference."""
        self.agent = agent
        self.logger = agent.logger

    def handle_coordination_message(self, message: dict[str, Any]) -> None:
        """
        Handle coordination message from another agent.

        Args:
            message: Coordination message dictionary

        Raises:
            ValueError: If message is invalid
        """
        if not isinstance(message, dict):
            raise ValueError("Message must be a dictionary")

        message_type = message.get("type", "unknown")

        try:
            if message_type == "resource_request":
                self.handle_resource_request(message)
            elif message_type == "activity_coordination":
                self.handle_activity_coordination(message)
            elif message_type == "emergency_alert":
                self.handle_emergency_alert(message)
            elif message_type == "status_update":
                self.handle_status_update(message)
            else:
                self.logger.warning(f"Unknown message type: {message_type}")

        except Exception as e:
            self.logger.error(
                f"Error handling coordination message type {message_type}: {e}",
                exc_info=True,
            )

    def handle_resource_request(self, message: dict[str, Any]) -> None:
        """
        Handle resource request from another agent.

        Args:
            message: Resource request message
        """
        try:
            requested_item = message.get("item")
            requesting_agent = message.get("from_agent")

            if not requested_item or not requesting_agent:
                self.logger.warning("Invalid resource request: missing item or agent")
                return

            self.logger.info(
                f"Resource request: {requested_item} from {requesting_agent}"
            )

            # Check if we have the requested resource
            has_resource = (
                self.agent.game_state
                and requested_item in self.agent.game_state.inventory_items
            )

            # Send response to requesting agent
            response = {
                "type": "resource_response",
                "item": requested_item,
                "available": has_resource,
                "from_agent": self.agent.agent_id,
            }

            self.agent.send_message(requesting_agent, response)

        except Exception as e:
            self.logger.error(f"Error handling resource request: {e}", exc_info=True)

    def handle_activity_coordination(self, message: dict[str, Any]) -> None:
        """
        Handle activity coordination message.

        Args:
            message: Activity coordination message
        """
        try:
            activity = message.get("activity")
            coordinating_agent = message.get("from_agent")

            if not activity:
                self.logger.warning("Invalid activity coordination: missing activity")
                return

            self.logger.info(
                f"Activity coordination: {activity} from {coordinating_agent}"
            )

            # Determine if we should participate
            if self.should_participate_in_activity(activity):
                self.agent.current_activity = activity
                self.logger.info(
                    f"Participating in coordinated activity: {activity}"
                )

                # Send confirmation to coordinating agent
                confirmation = {
                    "type": "activity_confirmation",
                    "activity": activity,
                    "from_agent": self.agent.agent_id,
                    "status": "participating",
                }
                self.agent.send_message(coordinating_agent, confirmation)

        except Exception as e:
            self.logger.error(
                f"Error handling activity coordination: {e}", exc_info=True
            )

    def handle_emergency_alert(self, message: dict[str, Any]) -> None:
        """
        Handle emergency alert from another agent.

        Args:
            message: Emergency alert message
        """
        try:
            emergency_type = message.get("emergency_type")
            alerting_agent = message.get("from_agent")

            if not emergency_type:
                self.logger.warning("Invalid emergency alert: missing type")
                return

            self.logger.warning(
                f"Emergency alert: {emergency_type} from {alerting_agent}"
            )

            # Take appropriate emergency response based on our role
            from .osrs_agent_core import AgentRole

            if self.agent.role == AgentRole.EMERGENCY_RESPONSE:
                self.initiate_emergency_response(emergency_type, alerting_agent)
            else:
                # Acknowledge emergency even if not emergency response role
                self.logger.info(
                    f"Acknowledging emergency {emergency_type} (role: {self.agent.role.value})"
                )

        except Exception as e:
            self.logger.error(f"Error handling emergency alert: {e}", exc_info=True)

    def handle_status_update(self, message: dict[str, Any]) -> None:
        """
        Handle status update from another agent.

        Args:
            message: Status update message
        """
        try:
            agent_id = message.get("from_agent")
            status = message.get("status")
            activity = message.get("activity")

            if not agent_id:
                self.logger.warning("Invalid status update: missing agent ID")
                return

            # Update other agent's status in our tracking
            if agent_id in self.agent.other_agents:
                self.agent.other_agents[agent_id]["status"] = status
                if activity:
                    self.agent.other_agents[agent_id]["activity"] = activity

            self.logger.debug(f"Status update from {agent_id}: {status}")

        except Exception as e:
            self.logger.error(f"Error handling status update: {e}", exc_info=True)

    def should_participate_in_activity(self, activity: str) -> bool:
        """
        Determine if this agent should participate in a coordinated activity.

        Args:
            activity: Activity description

        Returns:
            True if agent should participate
        """
        if not activity:
            return False

        try:
            from .osrs_agent_core import AgentRole

            activity_lower = activity.lower()

            # Role-based participation logic
            if self.agent.role == AgentRole.EMERGENCY_RESPONSE:
                return "emergency" in activity_lower or "critical" in activity_lower

            elif self.agent.role == AgentRole.COMBAT_SPECIALIST:
                return (
                    "combat" in activity_lower
                    or "pvp" in activity_lower
                    or "fighting" in activity_lower
                )

            elif self.agent.role == AgentRole.RESOURCE_MANAGER:
                return (
                    "resource" in activity_lower
                    or "gathering" in activity_lower
                    or "mining" in activity_lower
                    or "fishing" in activity_lower
                )

            elif self.agent.role == AgentRole.QUEST_COORDINATOR:
                return "quest" in activity_lower or "mission" in activity_lower

            elif self.agent.role == AgentRole.STRATEGIC_PLANNER:
                return "strategy" in activity_lower or "planning" in activity_lower

            elif self.agent.role == AgentRole.TRADING_SPECIALIST:
                return "trading" in activity_lower or "market" in activity_lower

            elif self.agent.role == AgentRole.SKILL_TRAINER:
                return "training" in activity_lower or "skill" in activity_lower

            elif self.agent.role == AgentRole.CLAN_COORDINATOR:
                return "clan" in activity_lower or "group" in activity_lower

            return False

        except Exception as e:
            self.logger.error(
                f"Error determining activity participation: {e}", exc_info=True
            )
            return False

    def initiate_emergency_response(
        self, emergency_type: str, alerting_agent: str
    ) -> None:
        """
        Initiate emergency response procedure.

        Args:
            emergency_type: Type of emergency
            alerting_agent: Agent that sent the alert
        """
        try:
            self.logger.critical(
                f"Initiating emergency response for {emergency_type} from {alerting_agent}"
            )

            # Broadcast emergency to all agents
            emergency_message = {
                "type": "emergency_broadcast",
                "emergency_type": emergency_type,
                "from_agent": self.agent.agent_id,
                "alerting_agent": alerting_agent,
                "priority": "urgent",
            }

            # Send to all known agents
            for agent_id in self.agent.other_agents.keys():
                if agent_id != self.agent.agent_id:
                    self.agent.send_message(agent_id, emergency_message)

            # Update agent status for emergency response
            from .osrs_agent_core import OSRSAgentStatus

            if self.agent.status != OSRSAgentStatus.ERROR:
                previous_status = self.agent.status
                self.agent.status = OSRSAgentStatus.ERROR
                self.logger.info(
                    f"Agent status changed: {previous_status} -> {OSRSAgentStatus.ERROR}"
                )

        except Exception as e:
            self.logger.error(f"Error initiating emergency response: {e}", exc_info=True)
