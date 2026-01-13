#!/usr/bin/env python3
"""
Unified Handler Base Class - Code Deduplication
===============================================

<!-- SSOT Domain: core -->

Consolidates repetitive handler patterns across the codebase.
Combines BaseService functionality with handler-specific patterns like:
- Command counting and metrics
- Command history tracking
- Standardized error handling
- Common initialization patterns

V2 Compliance: < 300 lines, single responsibility
Consolidates patterns from 15+ handler classes.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-11
"""

import logging
import time
from abc import ABC
from typing import Any, Dict, List, Optional

from .base_service import BaseService


class UnifiedHandler(BaseService, ABC):
    """
    Unified base class for all handler classes.

    Consolidates repetitive patterns found across handler implementations:
    - Command counting (total, successful, failed)
    - Command history tracking with standardized structure
    - Error handling and metrics
    - Common initialization patterns

    Usage:
        class MyHandler(UnifiedHandler):
            def __init__(self):
                super().__init__("MyHandler")
                # Custom initialization
    """

    def __init__(self, handler_name: str, max_history: int = 100):
        """
        Initialize unified handler with standardized patterns.

        Args:
            handler_name: Name of the handler for logging/metrics
            max_history: Maximum number of commands to keep in history
        """
        super().__init__(handler_name)

        # Command metrics - consolidated from multiple handlers
        self.command_count: int = 0
        self.successful_commands: int = 0
        self.failed_commands: int = 0

        # Command history - standardized structure across all handlers
        self.command_history: List[Dict[str, Any]] = []
        self.max_history = max_history

        self.logger.info(f"✅ {handler_name} handler initialized with metrics tracking")

    def can_handle(self, args) -> bool:
        """
        Check if this handler can handle the given arguments.

        Override in subclasses to implement specific handling logic.
        Default implementation returns False.

        Args:
            args: Arguments to check

        Returns:
            bool: True if this handler can handle the arguments
        """
        return False

    def record_command_start(self, command: str, args: Any = None) -> Dict[str, Any]:
        """
        Record the start of a command execution.

        Standardized command tracking across all handlers.

        Args:
            command: Command name being executed
            args: Arguments for the command

        Returns:
            dict: Command tracking data
        """
        self.command_count += 1
        start_time = time.time()

        command_data = {
            'command': command,
            'args': args,
            'start_time': start_time,
            'timestamp': start_time,
            'handler': self.service_name
        }

        return command_data

    def record_command_end(self, command_data: Dict[str, Any], success: bool,
                          result: Any = None, error: Optional[str] = None) -> None:
        """
        Record the completion of a command execution.

        Updates metrics and history with standardized structure.

        Args:
            command_data: Data from record_command_start
            success: Whether the command succeeded
            result: Result of the command (if any)
            error: Error message (if any)
        """
        execution_time = time.time() - command_data['start_time']

        # Update metrics
        if success:
            self.successful_commands += 1
        else:
            self.failed_commands += 1

        # Complete command data
        command_data.update({
            'success': success,
            'execution_time': execution_time,
            'end_time': time.time(),
            'result': result,
            'error': error
        })

        # Add to history
        self.command_history.append(command_data)

        # Maintain history size limit
        if len(self.command_history) > self.max_history:
            self.command_history.pop(0)

        # Log completion
        status = "✅" if success else "❌"
        self.logger.info(f"{status} Command '{command_data['command']}' completed "
                        ".3f"
                        f"({self.successful_commands}/{self.failed_commands})")

    async def execute_with_tracking(self, command: str, args: Any = None) -> Dict[str, Any]:
        """
        Execute a command with automatic tracking and error handling.

        Template method pattern for standardized command execution.

        Args:
            command: Command name to execute
            args: Arguments for the command

        Returns:
            dict: Execution result with tracking data
        """
        command_data = self.record_command_start(command, args)

        try:
            # Execute the actual command (to be implemented by subclasses)
            result = await self._execute_command(command, args)

            # Record success
            self.record_command_end(command_data, True, result)
            return result

        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Command '{command}' failed: {error_msg}")

            # Record failure
            self.record_command_end(command_data, False, error=error_msg)

            # Return standardized error response
            return {
                'success': False,
                'error': error_msg,
                'command': command,
                'execution_time': time.time() - command_data['start_time']
            }

    async def _execute_command(self, command: str, args: Any = None) -> Dict[str, Any]:
        """
        Execute the actual command logic.

        Must be implemented by subclasses.

        Args:
            command: Command to execute
            args: Command arguments

        Returns:
            dict: Command result

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement _execute_command")

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get handler metrics in standardized format.

        Returns:
            dict: Metrics data
        """
        return {
            'handler_name': self.service_name,
            'total_commands': self.command_count,
            'successful_commands': self.successful_commands,
            'failed_commands': self.failed_commands,
            'success_rate': (self.successful_commands / self.command_count) if self.command_count > 0 else 0,
            'history_size': len(self.command_history),
            'max_history': self.max_history
        }

    def get_command_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get command history, optionally limited.

        Args:
            limit: Maximum number of history items to return

        Returns:
            list: Command history
        """
        history = self.command_history
        if limit:
            history = history[-limit:]
        return history

    def reset_metrics(self) -> None:
        """Reset all command metrics and history."""
        self.command_count = 0
        self.successful_commands = 0
        self.failed_commands = 0
        self.command_history.clear()
        self.logger.info(f"✅ Metrics reset for {self.service_name}")