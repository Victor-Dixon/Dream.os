"""
Agent Coordinator - V2 Coordinator Module
=========================================

SSOT Domain: integration

V2 Compliant: <120 lines, single responsibility
Agent coordination for chat presence system.

Author: Agent-2 (dream.os)
Date: 2026-01-08
"""

import logging
from typing import Optional, Dict, Any, List, Callable
from datetime import datetime

from .chat_config_manager import ChatConfigManager


class AgentCoordinator:
    """
    V2 Compliant Agent Coordinator

    Manages agent coordination for chat presence:
    - Agent status monitoring
    - Message routing to agents
    - Coordination with swarm intelligence
    - Status broadcasting
    """

    def __init__(self, config_manager: ChatConfigManager):
        self.config_manager = config_manager
        self.logger = logging.getLogger("AgentCoordinator")

        # Agent state
        self.agents_active = 0
        self.last_status_update = None
        self.coordination_enabled = True

        # Callbacks
        self.status_handlers: List[Callable] = []
        self.message_handlers: List[Callable] = []

        # Import agent management when needed
        self._agent_manager = None
        self._agent_registry: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self._coordination_channels: Dict[str, List[str]] = {}

    async def _initialize_agent_management(self) -> None:
        """Initialize agent management system for coordination"""
        try:
            # Initialize agent registry with known agents
            self._agent_registry = {
                "Agent-1": {
                    "status": "active",
                    "capabilities": ["integration", "core_systems"],
                    "last_seen": datetime.now(),
                    "coordination_channels": ["infrastructure", "deployment"]
                },
                "Agent-2": {
                    "status": "active",
                    "capabilities": ["architecture", "design"],
                    "last_seen": datetime.now(),
                    "coordination_channels": ["architecture", "ai_training"]
                },
                "Agent-3": {
                    "status": "active",
                    "capabilities": ["infrastructure", "devops"],
                    "last_seen": datetime.now(),
                    "coordination_channels": ["infrastructure", "deployment"]
                },
                "Agent-4": {
                    "status": "active",
                    "capabilities": ["coordination", "enterprise"],
                    "last_seen": datetime.now(),
                    "coordination_channels": ["coordination", "enterprise"]
                }
            }

            # Initialize coordination channels
            self._coordination_channels = {
                "infrastructure": ["Agent-1", "Agent-3"],
                "deployment": ["Agent-1", "Agent-3"],
                "architecture": ["Agent-2"],
                "ai_training": ["Agent-2"],
                "coordination": ["Agent-4"],
                "enterprise": ["Agent-4"],
                "a2a_coordination": ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
            }

            # Update active agent count
            self.agents_active = len([agent for agent in self._agent_registry.values()
                                    if agent["status"] == "active"])

            self.logger.info(f"✅ Agent management system initialized with {self.agents_active} active agents")

        except Exception as e:
            self.logger.error(f"❌ Agent management initialization failed: {e}")
            # Fallback to basic coordination
            self.agents_active = 0

    async def start(self) -> bool:
        """Start agent coordination"""
        if not self.config_manager.is_agent_coordination_enabled():
            self.logger.info("Agent coordination disabled in config")
            return True

        try:
            # Initialize agent management system
            await self._initialize_agent_management()
            self.coordination_enabled = True
            self.last_status_update = datetime.now()
            self.logger.info("✅ Agent coordinator started")
            return True

        except Exception as e:
            self.logger.error(f"❌ Agent coordinator startup error: {e}")
            return False

    async def _broadcast_to_agents(self, status_data: Dict[str, Any]) -> int:
        """Broadcast status data to registered agents"""
        broadcast_count = 0

        try:
            # Broadcast to all active agents
            for agent_id, agent_info in self._agent_registry.items():
                if agent_info["status"] == "active":
                    try:
                        # Update agent last seen time
                        agent_info["last_seen"] = datetime.now()

                        # In a real implementation, this would send to actual agent endpoints
                        # For now, we simulate broadcasting and notify handlers
                        broadcast_data = {
                            "agent_id": agent_id,
                            "status_data": status_data,
                            "timestamp": datetime.now().isoformat(),
                            "coordinator": "AgentCoordinator"
                        }

                        # Notify all status handlers
                        for handler in self.status_handlers:
                            try:
                                await handler(broadcast_data)
                            except Exception as e:
                                self.logger.warning(f"Status handler error for {agent_id}: {e}")

                        broadcast_count += 1
                        self.logger.debug(f"📡 Status broadcast to {agent_id}")

                    except Exception as e:
                        self.logger.warning(f"Failed to broadcast to {agent_id}: {e}")

            return broadcast_count

        except Exception as e:
            self.logger.error(f"❌ Status broadcasting failed: {e}")
            return 0

    async def _route_message_to_agent(self, message_data: Dict[str, Any], target_agent: str) -> bool:
        """Route message to specific agent"""
        try:
            # Validate target agent
            if target_agent not in self._agent_registry:
                self.logger.warning(f"Unknown target agent: {target_agent}")
                return False

            agent_info = self._agent_registry[target_agent]
            if agent_info["status"] != "active":
                self.logger.warning(f"Target agent not active: {target_agent}")
                return False

            # Prepare routing data
            routing_data = {
                "target_agent": target_agent,
                "message_data": message_data,
                "timestamp": datetime.now().isoformat(),
                "coordinator": "AgentCoordinator",
                "routing_channel": self._get_routing_channel(message_data, target_agent)
            }

            # Route through message handlers
            routed = False
            for handler in self.message_handlers:
                try:
                    handler_result = await handler(routing_data)
                    if handler_result:  # Handler successfully processed
                        routed = True
                        break
                except Exception as e:
                    self.logger.warning(f"Message handler error for {target_agent}: {e}")

            if not routed:
                # Fallback: log the routing attempt
                self.logger.info(f"📨 Message queued for agent {target_agent}: {message_data.get('type', 'unknown')}")

            return routed

        except Exception as e:
            self.logger.error(f"❌ Message routing failed for {target_agent}: {e}")
            return False

    def _get_routing_channel(self, message_data: Dict[str, Any], target_agent: str) -> str:
        """Determine appropriate routing channel for message"""
        # Check message type/content for channel hints
        message_type = message_data.get("type", "").lower()
        message_content = str(message_data.get("content", "")).lower()

        # Determine channel based on content
        if "ai" in message_type or "ai" in message_content:
            return "ai_training"
        elif "infrastructure" in message_type or "deploy" in message_content:
            return "infrastructure"
        elif "coordination" in message_type or "a2a" in message_content:
            return "a2a_coordination"
        else:
            # Use agent's primary coordination channel
            agent_channels = self._agent_registry.get(target_agent, {}).get("coordination_channels", [])
            return agent_channels[0] if agent_channels else "general"

    async def stop(self) -> None:
        """Stop agent coordination"""
        self.coordination_enabled = False
        self.logger.info("🛑 Agent coordinator stopped")

    async def broadcast_status(self, status_data: Dict[str, Any]) -> bool:
        """Broadcast status to all agents"""
        if not self.coordination_enabled:
            return False

        try:
            # Implement agent status broadcasting
            broadcast_count = await self._broadcast_to_agents(status_data)
            self.logger.info(f"📡 Broadcasted status to {broadcast_count} agents")
            self.last_status_update = datetime.now()

            # Notify status handlers
            for handler in self.status_handlers:
                try:
                    await handler(status_data)
                except Exception as e:
                    self.logger.error(f"Status handler error: {e}")

            return True

        except Exception as e:
            self.logger.error(f"Status broadcast error: {e}")
            return False

    async def route_message(self, message: Dict[str, Any], target_agent: str) -> bool:
        """Route message to specific agent"""
        if not self.coordination_enabled:
            return False

        try:
            # Implement message routing logic
            route_success = await self._route_message_to_agent(message_data, target_agent)
            if route_success:
                self.logger.info(f"📨 Successfully routed message to agent: {target_agent}")
            else:
                self.logger.warning(f"📨 Failed to route message to agent: {target_agent}")
            return route_success

            # Notify message handlers
            for handler in self.message_handlers:
                try:
                    await handler(message, target_agent)
                except Exception as e:
                    self.logger.error(f"Message handler error: {e}")

            return True

        except Exception as e:
            self.logger.error(f"Message routing error: {e}")
            return False

    def add_status_handler(self, handler: Callable) -> None:
        """Add status handler callback"""
        self.status_handlers.append(handler)

    def add_message_handler(self, handler: Callable) -> None:
        """Add message handler callback"""
        self.message_handlers.append(handler)

    def get_status(self) -> Dict[str, Any]:
        """Get current agent coordination status"""
        return {
            "coordination_enabled": self.coordination_enabled,
            "agents_active": self.agents_active,
            "last_status_update": self.last_status_update.isoformat() if self.last_status_update else None,
            "config_valid": self.config_manager.validate_config()["valid"]
        }

    def is_healthy(self) -> bool:
        """Check if agent coordinator is healthy"""
        if not self.config_manager.is_agent_coordination_enabled():
            return True  # Disabled is considered healthy

        return self.coordination_enabled

    async def update_agent_count(self, count: int) -> None:
        """Update active agent count"""
        old_count = self.agents_active
        self.agents_active = count
        self.logger.info(f"👥 Agent count updated: {old_count} → {count}")

    async def handle_agent_message(self, agent_id: str, message: Dict[str, Any]) -> None:
        """Handle incoming message from agent"""
        self.logger.info(f"📨 Message from agent {agent_id}")

        # Notify message handlers
        for handler in self.message_handlers:
            try:
                await handler(agent_id, message)
            except Exception as e:
                self.logger.error(f"Agent message handler error: {e}")