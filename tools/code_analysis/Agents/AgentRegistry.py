"""
AgentRegistry.py

Manages the registration, retrieval, and lifecycle of AI agents dynamically.

Features:
  - Register, unregister, and retrieve AI agents.
  - Validate agents against the AgentBase structure.
  - Dynamically expand the registry for future AI agents.

Methods:
  - register_agent(name: str, agent_instance: AgentBase) -> bool
  - unregister_agent(name: str) -> bool
  - get_agent(name: str) -> Optional[AgentBase]
  - agent_exists(name: str) -> bool
  - list_agents() -> List[str]
"""

import logging
from typing import Dict, Optional, List

from utils.plugins.LoggerManager import LoggerManager

# Ensure proper import paths for core agents
try:
    from Agents.core.AgentBase import AgentBase
    from Agents.JournalAgent import JournalAgent
    from Agents.DebugAgent import DebugAgent
    from Agents.AIAgentWithMemory import AIAgentWithMemory
except ImportError as e:
    raise ImportError(f"❌ Agent module import failed: {e}")

# Initialize logger
logger = LoggerManager(log_file="agent_registry.log").get_logger()
logger.setLevel(logging.DEBUG)


class AgentRegistry:
    """
    Manages the registration, retrieval, and lifecycle of AI agents dynamically.
    """

    def __init__(self):
        self.agents: Dict[str, AgentBase] = {}
        self.load_core_agents()
        logger.info(f"✅ AgentRegistry initialized with agents: {self.list_agents()}")

    def load_core_agents(self) -> None:
        """
        Registers core AI agents on initialization.
        """
        core_agents = {
            "journalagent": JournalAgent(),
            "debugagent": DebugAgent(),
            "aiagentwithmemory": AIAgentWithMemory(
                name="aiagentwithmemory",
                project_name="DefaultProject",
                memory_manager=None,         # Provide an AgentMemory instance if available
                performance_monitor=None     # Provide a PerformanceMonitor instance if available
            ),
        }

        for name, agent in core_agents.items():
            registered = self.register_agent(name, agent)
            if not registered:
                logger.warning(f"⚠️ Failed to register core agent: {name}")

    def register_agent(self, name: str, agent_instance: AgentBase) -> bool:
        """
        Dynamically registers a new agent if it inherits from AgentBase.

        Args:
            name (str): The unique name of the agent.
            agent_instance (AgentBase): The agent instance.

        Returns:
            bool: True if registered successfully, False otherwise.
        """
        if not isinstance(agent_instance, AgentBase):
            logger.error(f"❌ Attempted to register invalid agent '{name}' (not an AgentBase subclass).")
            return False

        normalized_name = name.strip().lower()
        if normalized_name in self.agents:
            logger.warning(f"⚠️ Agent '{normalized_name}' is already registered.")
            return False

        self.agents[normalized_name] = agent_instance
        logger.info(f"✅ Agent '{normalized_name}' registered successfully.")
        return True

    def unregister_agent(self, name: str) -> bool:
        """
        Removes an agent from the registry.

        Args:
            name (str): The name of the agent to remove.

        Returns:
            bool: True if removed successfully, False if agent not found.
        """
        normalized_name = name.strip().lower()
        if normalized_name in self.agents:
            del self.agents[normalized_name]
            logger.info(f"🗑️ Agent '{normalized_name}' unregistered successfully.")
            return True

        logger.warning(f"⚠️ Attempted to remove non-existent agent '{normalized_name}'.")
        return False

    def get_agent(self, name: str) -> Optional[AgentBase]:
        """
        Retrieves an agent by name.

        Args:
            name (str): The name of the agent.

        Returns:
            Optional[AgentBase]: The agent instance if found, otherwise None.
        """
        normalized_name = name.strip().lower()
        agent = self.agents.get(normalized_name)
        if not agent:
            logger.warning(f"❌ Agent '{normalized_name}' not found in registry.")
        return agent

    def agent_exists(self, name: str) -> bool:
        """
        Checks if an agent exists in the registry.

        Args:
            name (str): The agent's name.

        Returns:
            bool: True if the agent exists, False otherwise.
        """
        return name.strip().lower() in self.agents

    def list_agents(self) -> List[str]:
        """
        Lists all registered agent names.

        Returns:
            List[str]: A list of available agent names.
        """
        return list(self.agents.keys())


# === ✅ Example Usage ===
if __name__ == "__main__":
    registry = AgentRegistry()
    logger.info(f"📋 Registered agents: {registry.list_agents()}")

    # Retrieve a specific agent (for example, DebugAgent)
    agent = registry.get_agent("debugagent")
    if agent:
        logger.info(f"🔍 Retrieved agent: {agent.name}")

    # Unregister an agent for demonstration
    if registry.unregister_agent("debugagent"):
        logger.info("✅ Agent 'debugagent' successfully unregistered.")

