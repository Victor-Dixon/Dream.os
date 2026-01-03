#!/usr/bin/env python
"""
CustomAgent.py

This module defines the CustomAgent class, a customizable AI agent that handles
user-defined tasks with flexible execution logic. It leverages persistent memory
(using ContextManager) to provide context-aware responses and learns from past interactions.
It inherits from AgentBase (from the integrated Agents/core module) to maintain consistency
with our robust agent infrastructure.

Key Methods:
  - __init__: Initializes the agent and sets up required resources.
  - solve_task: Processes a task and returns a structured result.
  - interact: Handles interactive queries by retrieving memory or generating a fallback reply.
  - describe_capabilities: Returns a description of the agent's capabilities.
  - shutdown: Performs cleanup and resource release.
"""

from typing import Any, Dict, Optional
from Agents.core.AgentBase import AgentBase
from Agents.ContextManager import ContextManager  # Local import to avoid circular dependencies
from utils.plugins.LoggerManager import LoggerManager

# Set up a logger for this module
logger = LoggerManager(log_file="custom_agent.log").get_logger()
logger.setLevel("DEBUG")


class CustomAgent(AgentBase):
    """
    CustomAgent is a flexible AI agent that:
      - Processes interactive queries with memory-based responses.
      - Handles custom-defined tasks via a simple task interface.
      - Learns from interactions by storing context for future use.
    """

    def __init__(self, name: str = "CustomAgent", project_name: str = "AI_Debugger_Assistant"):
        """
        Initializes the CustomAgent with a unique name and associates it with a project.
        
        Args:
            name (str): The name of the agent.
            project_name (str): The project or domain the agent is associated with.
        """
        super().__init__(name=name, project_name=project_name)
        # Reconfigure the logger for this agent instance if needed
        self.logger = LoggerManager(log_file=f"{self.name}.log").get_logger()
        self.logger.info(f"{self.name} initialized for project '{project_name}'.")

    def solve_task(self, task: str, **kwargs) -> Dict[str, Any]:
        """
        Processes a task and returns a structured result.
        
        For the 'interact' task, it checks its memory for a stored response or generates a fallback.
        For the 'describe' task, it returns a description of its capabilities.
        For other tasks, it returns an error message.
        
        Args:
            task (str): The task to perform.
            **kwargs: Additional parameters for task processing.
        
        Returns:
            dict: A dictionary with a status and the resulting response or error message.
        """
        self.logger.info(f"{self.name} received task: '{task}' with kwargs: {kwargs}")
        if task == "interact":
            query = kwargs.get("query", "")
            response = self.interact(query)
            return {"status": "success", "response": response}
        elif task == "describe":
            return {"status": "success", "description": self.describe_capabilities()}
        else:
            return {"status": "error", "message": f"Task '{task}' not recognized."}

    def interact(self, user_input: str) -> str:
        """
        Processes a user query by checking for a relevant past interaction in memory.
        If found, returns a context-aware response; otherwise, generates a fallback response,
        stores it in memory, and returns it.
        
        Args:
            user_input (str): The user's input or query.
        
        Returns:
            str: A context-aware response or a fallback message.
        """
        self.logger.info(f"{self.name} processing user input: '{user_input}'")
        memory_context = ContextManager.global_context.retrieve_memory(self.project_name, limit=5)
        if memory_context:
            response = f"(Context-Aware) {memory_context}"
            self.logger.info("Found relevant memory context.")
        else:
            response = "I'm still learning, but I'll remember this for next time!"
            ContextManager.global_context.store_memory(self.project_name, user_input, response)
            self.logger.info("Stored new interaction in memory.")
        return response

    def describe_capabilities(self) -> str:
        """
        Provides a description of the agent's capabilities.
        
        Returns:
            str: A brief description of what the agent can do.
        """
        capabilities = (
            "CustomAgent: Handles interactive queries with memory-based context, "
            "processes custom tasks, and learns from interactions."
        )
        self.logger.debug(f"{self.name} capabilities: {capabilities}")
        return capabilities

    def shutdown(self) -> None:
        """
        Shuts down the agent, releasing any allocated resources.
        """
        self.logger.info(f"{self.name} is shutting down. Releasing resources...")


# ==============================
# Example Usage
# ==============================
if __name__ == "__main__":
    # For demonstration purposes, instantiate and test the CustomAgent.
    agent = CustomAgent(name="CustomAgentDemo", project_name="DemoProject")
    print(agent.describe_capabilities())
    # Simulate an interactive task
    task_result = agent.solve_task("interact", query="What is the current status?")
    print(task_result)
    agent.shutdown()
