#!/usr/bin/env python
"""
AIAgentWithMemory.py

This module defines the AIAgentWithMemory class, which represents an AI agent that:
  - Interacts with users and retains memory of past conversations.
  - Provides context-aware responses.
  - Improves itself based on performance feedback.

It integrates with:
  - MemoryManager: For storing and retrieving conversation history.
  - PerformanceMonitor: For logging performance metrics.
  - AIModelManager: To use various AI models (DeepSeek, Mistral, OpenAI).
  - AgentBase: Ensures all agents follow a unified structure.

Usage:
  Instantiate AIAgentWithMemory with the required managers and call its async `solve_task` method.
"""

import asyncio
import logging
from typing import Dict, Any

# Import project modules (adjust paths as needed)
from Agents.core.AgentBase import AgentBase
from utils.plugins.LoggerManager import LoggerManager
from utils.plugins.AgentMemory import AgentMemory
from utils.plugins.PerformanceMonitor import PerformanceMonitor
from utils.plugins.AIModelManager import AIModelManager  # Handles AI model selection

logger = LoggerManager(log_file="ai_agent_with_memory.log").get_logger()


class AIAgentWithMemory(AgentBase):
    """
    AIAgentWithMemory represents an AI agent that:
      - Interacts with users.
      - Retains memory of past conversations.
      - Provides context-aware responses.
      - Self-improves based on performance metrics.

    Integrates:
      - MemoryManager for handling conversation memory.
      - PerformanceMonitor for tracking performance.
      - AIModelManager for selecting and managing AI models dynamically.
    """

    def __init__(
        self,
        name: str = "AIAgentWithMemory",
        project_name: str = "DefaultProject",
        memory_manager: AgentMemory = None,
        performance_monitor: PerformanceMonitor = None,
        ai_model_manager: AIModelManager = None,
    ):
        """
        Initialize the AI agent with a name, project name, MemoryManager, PerformanceMonitor, and AIModelManager.

        Args:
            name (str): Name of the AI agent.
            project_name (str): Project/domain the agent is associated with.
            memory_manager (AgentMemory): Handles conversation memory.
            performance_monitor (PerformanceMonitor): Tracks agent performance.
            ai_model_manager (AIModelManager): Manages AI models dynamically.
        """
        super().__init__(name, project_name)
        self.memory_manager = memory_manager or AgentMemory("memory.json")
        self.performance_monitor = performance_monitor or PerformanceMonitor("performance.log")
        self.ai_model_manager = ai_model_manager or AIModelManager()

        logger.info(f"Initialized AI Agent '{self.name}' for project '{self.project_name}'.")

    async def solve_task(self, task: str, **kwargs) -> str:
        """
        Solves a given task using memory and AI model reasoning.

        Args:
            task (str): The task description or user query.
            **kwargs: Additional parameters for the task.

        Returns:
            str: Response from the AI model or an error message.
        """
        try:
            # Retrieve memory context for the current project
            memory_context = self.memory_manager.retrieve_memory(self.project_name, limit=5)
            complete_prompt = f"{memory_context}\nUser: {task}\nAI:"

            logger.debug(f"Complete prompt sent to AI:\n{complete_prompt}")

            # Use the selected AI model (DeepSeek, Mistral, OpenAI)
            selected_model = self.ai_model_manager.get_active_model()
            response = await selected_model.generate_fix("User Query", complete_prompt)

            if not response:
                error_message = "❌ AI model failed to generate a response."
                logger.error(error_message)
                self.performance_monitor.log_performance(self.name, task, success=False, response=error_message)
                return error_message

            logger.info(f"Received AI response for task '{task}': {response}")

            # Save interaction to memory
            self.memory_manager.save_interaction(self.project_name, task, response)

            # Log successful response
            self.performance_monitor.log_performance(self.name, task, success=True, response=response)

            return response

        except Exception as ex:
            error_message = f"❌ Unexpected error: {str(ex)}"
            logger.error(error_message)
            self.performance_monitor.log_performance(self.name, task, success=False, response=error_message)
            return error_message

    def describe_capabilities(self) -> str:
        """
        Returns a description of the agent's capabilities.

        Returns:
            str: Capabilities description.
        """
        capabilities = (
            f"{self.name} can interact with users, retain memory, provide context-aware responses, "
            "dynamically switch AI models, and self-improve based on performance metrics."
        )
        logger.info("Capabilities described.")
        return capabilities

    def self_improve(self) -> None:
        """
        Analyzes performance metrics and triggers self-improvement actions.
        """
        analysis = self.performance_monitor.analyze_performance(self.name)
        if not analysis:
            logger.info("No performance data available for self-improvement.")
            return

        success_rate = analysis.get('success_rate', 0)
        failures = analysis.get('failures', 0)
        logger.debug(f"Self-improvement analysis: {analysis}")

        if success_rate < 80 and failures > 20:
            common_failure = max(
                analysis.get('failure_details', {}), 
                key=analysis.get('failure_details', {}).get, 
                default="Unknown"
            )
            logger.warning(f"Common failure reason: {common_failure}")
            self.take_action_based_on_failure(common_failure)
        else:
            logger.info("Performance satisfactory. No immediate improvements required.")

    def take_action_based_on_failure(self, reason: str) -> None:
        """
        Takes corrective actions based on a common failure reason.

        Args:
            reason (str): Identified common failure reason.
        """
        logger.info(f"Taking action based on failure: {reason}")
        suggestions = {
            "communication": "Check network connection or restart AI model service.",
            "permission": "Verify file and directory permissions.",
            "timeout": "Increase timeout threshold or optimize query.",
        }
        suggestion = suggestions.get(reason.lower(), "Review logs for detailed issues.")
        logger.info(f"Suggested improvement: {suggestion}")
        print(f"AI Suggestion: {suggestion}")


# === Example Usage ===
if __name__ == "__main__":
    # Instantiate required managers
    memory_manager = AgentMemory("memory.json")
    performance_monitor = PerformanceMonitor("performance.log")
    ai_model_manager = AIModelManager()  # Auto-selects best model (DeepSeek, Mistral, OpenAI)

    ai_agent = AIAgentWithMemory(
        name="ContextAwareAgent",
        project_name="MyProject",
        memory_manager=memory_manager,
        performance_monitor=performance_monitor,
        ai_model_manager=ai_model_manager
    )

    # Run an example task
    async def run_example():
        response = await ai_agent.solve_task("What is the weather like today?")
        print(f"AI Response: {response}")

    asyncio.run(run_example())
