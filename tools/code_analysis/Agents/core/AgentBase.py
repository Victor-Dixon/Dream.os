# D:\AgentProject\Agents\core\AgentBase.py

"""
AgentBase.py

Consolidated module that defines a robust, extensible base for AI-driven agents,
alongside integrated agent classes such as AgentRegistry, AgentActor, AIAgent,
AIAgentWithMemory, and CustomAgent.

Features:
    - Unified base class (AgentBase) with advanced functionalities:
        * Structured logging via LoggerManager
        * Memory management (optional)
        * Performance monitoring (optional)
        * Dynamic plugin loading
        * Error handling
        * Task scheduling (cron-based)
        * Chain-of-thought reasoning integration (optional)
    - Agent registry for managing multiple agents.
    - AI model manager to switch between DeepSeek, Mistral, and OpenAI.
    - Specialized agent classes: CustomAgent, (DebugAgent, JournalAgent if implemented),
      AIAgentWithMemory.
    - AI patch utilities for code patching (integrated via plugins).

Usage:
    Subclass AgentBase (or use one of the integrated specialized agents) to implement
    custom logic. Example usage is provided in the __main__ section.
"""

import abc
import asyncio
import json
import logging
import subprocess
import traceback
from typing import Any, Dict, Optional, List

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# === External project modules ===
from utils.plugins.LoggerManager import LoggerManager
from utils.plugins.PatchTrackingManager import PatchTrackingManager
from utils.plugins.AIConfidenceManager import AIConfidenceManager
from utils.plugins.AIModelManager import AIModelManager
from utils.plugins.AgentMemory import AgentMemory
from utils.plugins.PerformanceMonitor import PerformanceMonitor
from utils.plugins.AgentPlugin import AgentPlugin

# =====================================
# Global Logger Setup (for sample usage)
# =====================================
logger = LoggerManager(log_file="agent_base.log").get_logger()
logger.setLevel("DEBUG")


# =====================================
# Base Agent Class
# =====================================
class AgentBase(abc.ABC):
    """
    AgentBase serves as a comprehensive base class for all AI-driven agents.
    It integrates:
        - Task scheduling (cron-based)
        - Structured logging (via LoggerManager)
        - Memory management (optional)
        - Performance monitoring (optional)
        - Dynamic plugin support
        - Error handling
        - Chain-of-thought reasoning (optional)

    Subclasses must implement the abstract method `solve_task` to define task-specific logic.
    """

    MAX_RETRIES = 3
    SIMILARITY_THRESHOLD = 0.75

    def __init__(
        self,
        name: str = "GenericAgent",
        description: str = "",
        project_name: str = "",
        plugin_dir: str = "plugins",
        memory_manager: Optional[Any] = None,
        performance_monitor: Optional[Any] = None,
        log_to_file: bool = False,
        reasoner: Optional[Any] = None,
    ):
        self.name = name
        self.description = description
        self.project_name = project_name
        self.plugin_dir = plugin_dir
        self.memory_manager = memory_manager
        self.performance_monitor = performance_monitor
        self.reasoner = reasoner

        # Create a dedicated logger for this agent
        self.logger = LoggerManager(log_file=f"{self.name}.log").get_logger()
        self.logger.info(f"Initialized Agent '{self.name}' for project '{self.project_name}'.")

        # Start a background scheduler for periodic tasks
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    @abc.abstractmethod
    def solve_task(self, task_data: Dict[str, Any]) -> str:
        """
        Abstract method to solve a given task. Must be implemented by subclasses.

        Args:
            task_data (Dict[str, Any]): Details about the task to solve.

        Returns:
            str: The result or output of solving the task.
        """
        pass

    def shutdown(self):
        """Gracefully shuts down the agent and its scheduler."""
        self.scheduler.shutdown()
        self.logger.info(f"Agent '{self.name}' shutdown completed.")


# =====================================
# AgentRegistry Class
# =====================================
class AgentRegistry:
    """
    Manages the registration, retrieval, and lifecycle of AI agents dynamically.
    """

    def __init__(self):
        self.agents: Dict[str, AgentBase] = {}
        self.logger = LoggerManager(log_file="agent_registry.log").get_logger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.info("AgentRegistry initialized.")

    def register_agent(self, name: str, agent_instance: AgentBase) -> bool:
        """
        Dynamically registers a new agent if it inherits from AgentBase.
        """
        if not isinstance(agent_instance, AgentBase):
            self.logger.error(f"❌ Attempted to register invalid agent '{name}' (not an AgentBase subclass).")
            return False

        normalized_name = name.strip().lower()
        if normalized_name in self.agents:
            self.logger.warning(f"⚠️ Agent '{normalized_name}' is already registered.")
            return False

        self.agents[normalized_name] = agent_instance
        self.logger.info(f"✅ Agent '{normalized_name}' registered successfully.")
        return True

    def unregister_agent(self, name: str) -> bool:
        """
        Removes an agent from the registry.
        """
        normalized_name = name.strip().lower()
        if normalized_name in self.agents:
            del self.agents[normalized_name]
            self.logger.info(f"🗑️ Agent '{normalized_name}' unregistered successfully.")
            return True

        self.logger.warning(f"⚠️ Attempted to remove non-existent agent '{normalized_name}'.")
        return False

    def get_agent(self, name: str) -> Optional[AgentBase]:
        """
        Retrieves an agent by name.
        """
        normalized_name = name.strip().lower()
        agent = self.agents.get(normalized_name)
        if not agent:
            self.logger.warning(f"❌ Agent '{normalized_name}' not found in registry.")
        return agent

    def list_agents(self) -> List[str]:
        """
        Lists all registered agent names.
        """
        return list(self.agents.keys())

# =====================================
# AgentActor Class
# =====================================
class AgentActor:
    """
    Executes tasks and manages tool operations via a ToolServer.
    Integrates with memory and performance monitoring.
    """

    def __init__(self, tool_server: Any, memory_manager: AgentMemory, performance_monitor: PerformanceMonitor):
        self.logger = LoggerManager(log_file="agent_actor.log").get_logger()
        self.tool_server = tool_server
        self.memory_manager = memory_manager
        self.performance_monitor = performance_monitor
        self.logger.info("AgentActor initialized.")

    def describe_capabilities(self) -> str:
        return "AgentActor can execute Python code, run shell commands, and utilize specialized tools."

    def solve_task(self, task: str) -> str:
        self.logger.info(f"Received task: {task}")
        if task.lower().startswith("python:"):
            return self._execute_python_task(task[len("python:"):].strip())
        else:
            return self._execute_shell_task(task)

    def _execute_python_task(self, python_code: str) -> str:
        try:
            result = self.tool_server.python_notebook.execute_code(python_code)
            self.logger.info("Executed Python code successfully.")
            self.performance_monitor.record("python_task", python_code, success=True)
            return result
        except Exception as e:
            error_msg = f"Python execution failed: {str(e)}"
            self.logger.error(error_msg)
            self.performance_monitor.record("python_task", python_code, success=False, response=error_msg)
            return error_msg

    def _execute_shell_task(self, command: str) -> str:
        try:
            result = self.tool_server.shell.execute_command(command)
            self.logger.info("Executed shell command successfully.")
            self.performance_monitor.record("shell_task", command, success=True)
            return result
        except Exception as e:
            error_msg = f"Shell execution failed: {str(e)}"
            self.logger.error(error_msg)
            self.performance_monitor.record("shell_task", command, success=False, response=error_msg)
            return error_msg

    def shutdown(self) -> None:
        self.logger.info("AgentActor is shutting down. Releasing resources...")


# =====================================
# AIAgent Class and Plugin Interface
# =====================================
class PluginInterface:
    """
    Example plugin interface.
    Concrete plugins should subclass this interface and implement `execute(command)`.
    """
    def execute(self, command: str) -> str:
        raise NotImplementedError("Plugins must implement `execute()`.")


class AIAgent:
    """
    AIAgent manages a collection of plugins, each providing specific capabilities.
    The agent acts as a central dispatcher for plugin commands.
    """

    def __init__(self):
        self.plugins = {}
        self.logger = LoggerManager(log_file="ai_agent.log").get_logger()
        self.logger.info("AIAgent initialized with no plugins.")

    def register_plugin(self, name: str, plugin: PluginInterface):
        if not hasattr(plugin, 'execute') or not callable(plugin.execute):
            raise ValueError(f"Plugin '{name}' must implement an `execute` method.")
        self.plugins[name] = plugin
        self.logger.info(f"Plugin '{name}' registered.")

    def execute(self, plugin_name: str, command: str) -> str:
        if plugin_name not in self.plugins:
            raise ValueError(f"Plugin '{plugin_name}' not found in agent's registry.")
        self.logger.debug(f"Executing command '{command}' using plugin '{plugin_name}'.")
        return self.plugins[plugin_name].execute(command)


# =====================================
# AIAgentWithMemory Class
# =====================================
class AIAgentWithMemory(AgentPlugin):
    """
    Represents an AI agent that can interact with users, retain conversation memory,
    provide context-aware responses, and self-improve based on performance metrics.
    """

    def __init__(
        self,
        name: str,
        project_name: str,
        memory_manager: AgentMemory,
        performance_monitor: PerformanceMonitor,
    ):
        super().__init__(name=name)
        self.logger = LoggerManager(log_file="ai_agent_with_memory.log").get_logger()
        self.project_name = project_name
        self.memory_manager = memory_manager
        self.performance_monitor = performance_monitor
        self.logger.info(f"Initialized AI Agent '{self.name}' for project '{self.project_name}'.")

    async def solve_task(self, task: str, **kwargs) -> str:
        try:
            memory_context = self.memory_manager.retrieve_memory(self.project_name, limit=5)
            complete_prompt = f"{memory_context}\nUser: {task}\nAI:"
            self.logger.debug(f"Complete prompt:\n{complete_prompt}")

            process = await asyncio.create_subprocess_exec(
                "ollama", "run", "mistral:latest", "--prompt", complete_prompt,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                err = stderr.decode().strip() or "Unknown error"
                self.logger.error(f"Error from AI model: {err}")
                self.performance_monitor.log_performance(self.name, task, success=False, response=err)
                return f"An error occurred: {err}"

            response = stdout.decode().strip()
            self.logger.info(f"Received AI response: {response}")
            self.memory_manager.save_interaction(self.project_name, task, response)
            self.performance_monitor.log_performance(self.name, task, success=True, response=response)
            return response
        except Exception as ex:
            error = f"Unexpected error: {ex}"
            self.logger.error(error)
            self.performance_monitor.log_performance(self.name, task, success=False, response=error)
            return error

    def describe_capabilities(self) -> str:
        text = (
            f"{self.name} can interact with users, retain memory, provide context-aware responses, "
            "and self-improve based on performance metrics."
        )
        self.logger.info("Capabilities described.")
        return text

    def self_improve(self) -> None:
        analysis = self.performance_monitor.analyze_performance(self.name)
        if not analysis:
            self.logger.info("No performance data for self-improvement.")
            return
        success_rate = analysis.get('success_rate', 0)
        failures = analysis.get('failures', 0)
        self.logger.debug(f"Self-improvement analysis: {analysis}")

        if success_rate < 80 and failures > 20:
            reason = max(analysis.get('failure_details', {}), key=analysis['failure_details'].get, default="Unknown")
            self.logger.warning(f"Common failure reason: {reason}")
            self.take_action_based_on_failure(reason)
        else:
            self.logger.info("Performance satisfactory. No immediate improvements required.")

    def take_action_based_on_failure(self, reason: str) -> None:
        suggestions = {
            "communication": "Check network or model service.",
            "permission": "Check file/directory permissions.",
            "timeout": "Increase timeout or optimize query.",
        }
        self.logger.info(f"Taking action based on failure: {reason}")
        suggestion = suggestions.get(reason.lower(), "Review logs for details.")
        self.logger.info(f"Suggested improvement: {suggestion}")


# =====================================
# CustomAgent Class
# =====================================
class CustomAgent(AgentBase):
    """
    CustomAgent is a flexible AI agent that:
      - Processes interactive queries with memory-based responses.
      - Handles custom-defined tasks via a simple task interface.
      - Learns from interactions by storing context for future use.
    """

    def __init__(self, name: str = "CustomAgent", project_name: str = "AI_Debugger_Assistant"):
        super().__init__(name=name, project_name=project_name)
        self.logger = LoggerManager(log_file=f"{self.name}.log").get_logger()
        self.logger.info(f"{self.name} initialized for project '{project_name}'.")

    def solve_task(self, task: str, **kwargs) -> Dict[str, Any]:
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
        from Agents.ContextManager import ContextManager  # local import to avoid circular dependencies
        self.logger.info(f"{self.name} processing user input: '{user_input}'")
        memory_context = ContextManager.global_context.retrieve_memory(self.project_name, limit=5)
        if memory_context:
            response = f"(Context-Aware) {memory_context}"
            self.logger.info("Found relevant memory context.")
        else:
            response = "I'm still learning. I'll remember this for next time."
            ContextManager.global_context.store_memory(self.project_name, user_input, response)
            self.logger.info("Stored new interaction in memory.")
        return response

    def describe_capabilities(self) -> str:
        capabilities = ("CustomAgent: Handles interactive queries with memory-based context, "
                        "processes custom tasks, and learns from interactions.")
        self.logger.debug(f"{self.name} capabilities: {capabilities}")
        return capabilities

    def shutdown(self) -> None:
        self.logger.info(f"{self.name} is shutting down. Releasing resources...")


# =====================================
# Example Usage of Integrated Agent System
# =====================================
if __name__ == "__main__":
    import sys
    import threading
    import time
    from PyQt5.QtWidgets import QApplication

    logging.info("=== Example usage of Merged Agent System ===")

    # Create an AgentRegistry and register the sample agent.
    registry = AgentRegistry()
    sample_agent = CustomAgent(name="SampleAgent", project_name="DemoProject")
    registry.register_agent("custom", sample_agent)
    logging.info(f"Currently registered agents: {registry.list_agents()}")

    # Test a simple interactive task.
    result = sample_agent.solve_task("interact", query="Hello, agent!")
    logging.info(f"CustomAgent task result: {result}")

    # Optional: Launch a GUI if desired (requires proper setup and PyQt5)
    """
    app = QApplication(sys.argv)
    from Agents.core.utilities.agent_gui import AgentGUI  # Adjust path as needed
    gui = AgentGUI(sample_agent)
    gui.show()

    def run_scheduler():
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            sample_agent.shutdown()

    threading.Thread(target=run_scheduler, daemon=True).start()
    sys.exit(app.exec_())
    """

    sample_agent.shutdown()
    logging.info("=== Integrated Agent System usage complete. ===")
