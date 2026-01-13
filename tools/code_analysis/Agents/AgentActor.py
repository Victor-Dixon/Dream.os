"""
AgentActor.py

This module defines the AgentActor class which executes tasks and manages tool operations via
a ToolServer. It leverages our centralized LoggerManager, AgentMemory, and PerformanceMonitor.
AgentActor supports executing Python code, shell commands, and utilizing specialized tools.

Key Methods:
  - describe_capabilities: Returns a description of what the agent can do.
  - solve_task: Routes tasks based on type (e.g., "python:" prefix for Python code).
  - _execute_python_task: Executes Python code via ToolServer's python_notebook.
  - _execute_shell_task: Executes shell commands via ToolServer's shell.
  - utilize_tool: Invokes a specific operation on a tool provided by ToolServer.
  - shutdown: Performs cleanup.
"""

import os
import logging
import subprocess
from typing import Any, Dict

# Import our centralized modules (adjust paths as needed)
from utils.plugins.LoggerManager import LoggerManager
from utils.plugins.AgentMemory import AgentMemory
from utils.plugins.PerformanceMonitor import PerformanceMonitor

logger = LoggerManager(log_file="agent_actor.log").get_logger()


class AgentActor:
    """
    Executes tasks and manages tool operations via a ToolServer.

    Integrates with AgentMemory to track task history and PerformanceMonitor to log execution metrics.
    Tasks may include executing Python code, shell commands, or using specialized tools.
    """

    def __init__(self, tool_server: Any, memory_manager: AgentMemory, performance_monitor: PerformanceMonitor):
        """
        Initializes AgentActor with a tool server, memory manager, and performance monitor.

        Args:
            tool_server (Any): An instance of ToolServer providing access to tools (e.g., python_notebook, shell).
            memory_manager (AgentMemory): Manages task memory and historical interactions.
            performance_monitor (PerformanceMonitor): Tracks performance metrics for task executions.
        """
        self.tool_server = tool_server
        self.memory_manager = memory_manager
        self.performance_monitor = performance_monitor
        logger.info("AgentActor initialized.")

    def describe_capabilities(self) -> str:
        """
        Returns a description of the agent's capabilities.
        """
        return "AgentActor can execute Python code, run shell commands, and utilize specialized tools."

    def solve_task(self, task: str) -> str:
        """
        Executes a given task based on its type.
        If the task starts with 'python:', it is executed as Python code.
        Otherwise, it is executed as a shell command.
        
        Args:
            task (str): The task to execute.
        
        Returns:
            str: Result of the task execution.
        """
        logger.info(f"Received task: {task}")
        if task.lower().startswith("python:"):
            python_code = task[len("python:"):].strip()
            result = self._execute_python_task(python_code)
        else:
            result = self._execute_shell_task(task)
        
        logger.debug(f"Task result: {result}")
        return result

    def _execute_python_task(self, python_code: str) -> str:
        """
        Executes Python code using the ToolServer's python_notebook.
        
        Args:
            python_code (str): Python code to execute.
        
        Returns:
            str: Result from executing the Python code or an error message.
        """
        try:
            result = self.tool_server.python_notebook.execute_code(python_code)
            logger.info("Executed Python code successfully.")
            self.performance_monitor.record("python_task", python_code, success=True)
            return result
        except Exception as e:
            error_msg = f"Python execution failed: {str(e)}"
            logger.error(error_msg)
            self.performance_monitor.record("python_task", python_code, success=False, response=error_msg)
            return error_msg

    def _execute_shell_task(self, command: str) -> str:
        """
        Executes a shell command using the ToolServer's shell tool.
        
        Args:
            command (str): The shell command to execute.
        
        Returns:
            str: Output from the shell command or an error message.
        """
        try:
            result = self.tool_server.shell.execute_command(command)
            logger.info("Executed shell command successfully.")
            self.performance_monitor.record("shell_task", command, success=True)
            return result
        except Exception as e:
            error_msg = f"Shell execution failed: {str(e)}"
            logger.error(error_msg)
            self.performance_monitor.record("shell_task", command, success=False, response=error_msg)
            return error_msg

    def utilize_tool(self, tool_name: str, operation: str, parameters: Dict[str, Any]) -> Any:
        """
        Uses a specified tool from the ToolServer by calling its operation with parameters.
        
        Args:
            tool_name (str): The name of the tool in ToolServer.
            operation (str): The operation method to invoke on the tool.
            parameters (Dict[str, Any]): Parameters to pass to the operation.
        
        Returns:
            Any: The result of the tool operation or an error message.
        """
        try:
            tool = getattr(self.tool_server, tool_name, None)
            if not tool:
                error_msg = f"Tool '{tool_name}' not found in ToolServer."
                logger.error(error_msg)
                return error_msg

            tool_method = getattr(tool, operation, None)
            if not callable(tool_method):
                error_msg = f"Operation '{operation}' not found in tool '{tool_name}'."
                logger.error(error_msg)
                return error_msg

            result = tool_method(**parameters)
            logger.info(f"Operation '{operation}' on tool '{tool_name}' executed successfully.")
            self.performance_monitor.record("tool_task", f"{tool_name}.{operation}", success=True)
            return result
        except Exception as e:
            error_msg = f"Failed to execute operation '{operation}' on tool '{tool_name}': {str(e)}"
            logger.error(error_msg)
            self.performance_monitor.record("tool_task", f"{tool_name}.{operation}", success=False, response=error_msg)
            return error_msg

    def perform_task(self, task: Dict[str, Any]) -> str:
        """
        Executes a task based on its type, which may be 'python' or 'shell'.
        
        Args:
            task (Dict[str, Any]): Dictionary with keys 'type' and 'content'.
        
        Returns:
            str: Result of the task execution.
        """
        task_type = task.get("type")
        content = task.get("content", "")
        if not task_type:
            return "Error: Task type is missing."
        if task_type.lower() == "python":
            return self._execute_python_task(content)
        elif task_type.lower() == "shell":
            return self._execute_shell_task(content)
        else:
            return f"Error: Unsupported task type '{task_type}'."

    def shutdown(self) -> None:
        """
        Performs any necessary cleanup operations.
        """
        logger.info("AgentActor is shutting down. Releasing resources...")
