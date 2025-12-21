"""
Command Execution Wrapper - SSOT for Command Execution with Completion Detection

<!-- SSOT Domain: infrastructure -->

===============================================================================

Wraps command execution with automatic completion detection.
Single Source of Truth for all command execution.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-01-27
V2 Compliance: <400 lines
"""

import logging
import subprocess
from typing import Any, Dict, Optional, Tuple

from .task_completion_detector import get_completion_detector, detect_command_completion

logger = logging.getLogger(__name__)


class CommandExecutionResult:
    """Result of command execution."""

    def __init__(
        self,
        command: str,
        exit_code: int,
        stdout: str,
        stderr: str,
        is_complete: bool,
        completion_reason: Optional[str] = None,
    ):
        """Initialize result."""
        self.command = command
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr
        self.is_complete = is_complete
        self.completion_reason = completion_reason
        self.success = exit_code == 0 and is_complete

    def __bool__(self) -> bool:
        """Return True if command succeeded."""
        return self.success

    def __str__(self) -> str:
        """String representation."""
        status = "✅ SUCCESS" if self.success else "❌ FAILED"
        return f"{status} [{self.exit_code}] {self.command[:50]}..."


def execute_command_with_completion(
    command: str,
    shell: bool = True,
    timeout: Optional[int] = None,
    check_completion: bool = True,
    task_id: Optional[str] = None,
) -> CommandExecutionResult:
    """
    Execute command with automatic completion detection.
    
    Args:
        command: Command to execute
        shell: Use shell execution
        timeout: Command timeout in seconds
        check_completion: Enable completion detection
        task_id: Optional task ID for tracking
        
    Returns:
        CommandExecutionResult with completion status
    """
    detector = get_completion_detector()

    # Register task if ID provided
    if task_id:
        detector.register_task(
            task_id,
            task_type="command",
            timeout=timeout or 300,
            success_patterns=["complete", "done", "success", "✅"],
            failure_patterns=["error", "failed", "❌", "exception"],
        )

    try:
        # Execute command
        process = subprocess.Popen(
            command,
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

        stdout_lines = []
        stderr_lines = []

        # Read output line by line
        while True:
            # Check stdout
            if process.stdout:
                line = process.stdout.readline()
                if line:
                    stdout_lines.append(line)
                    output_so_far = "".join(stdout_lines)

                    # Check for completion if enabled
                    if check_completion and task_id:
                        is_complete, reason = detector.detect_output_completion(output_so_far)
                        if is_complete:
                            logger.debug(f"Command completion detected: {reason}")
                            # Continue reading but mark as complete

            # Check stderr
            if process.stderr:
                line = process.stderr.readline()
                if line:
                    stderr_lines.append(line)

            # Check if process finished
            if process.poll() is not None:
                break

        # Wait for process to complete
        exit_code = process.wait(timeout=timeout)

        # Get final output
        stdout = "".join(stdout_lines)
        stderr = "".join(stderr_lines)
        full_output = stdout + stderr

        # Detect completion
        is_complete = False
        completion_reason = None

        if check_completion:
            # Check exit code first
            if exit_code == 0:
                is_complete, completion_reason = detect_command_completion(full_output)
                if not is_complete:
                    # Exit code 0 but no completion pattern - assume success
                    is_complete = True
                    completion_reason = "Exit code 0"
            else:
                # Non-zero exit code - check for error patterns
                is_complete, completion_reason = detect_command_completion(full_output)
                if not is_complete:
                    # Non-zero exit but no pattern - assume failed
                    is_complete = True
                    completion_reason = f"Exit code {exit_code}"

        # Update task if registered
        if task_id:
            detector.update_task_output(task_id, full_output, exit_code)

        result = CommandExecutionResult(
            command=command,
            exit_code=exit_code,
            stdout=stdout,
            stderr=stderr,
            is_complete=is_complete,
            completion_reason=completion_reason,
        )

        logger.debug(f"Command executed: {result}")
        return result

    except subprocess.TimeoutExpired:
        logger.error(f"Command timeout: {command}")
        return CommandExecutionResult(
            command=command,
            exit_code=-1,
            stdout="".join(stdout_lines),
            stderr="".join(stderr_lines),
            is_complete=True,
            completion_reason="Timeout",
        )

    except Exception as e:
        logger.error(f"Command execution failed: {e}")
        return CommandExecutionResult(
            command=command,
            exit_code=-1,
            stdout="",
            stderr=str(e),
            is_complete=True,
            completion_reason=f"Exception: {e}",
        )


def wait_for_completion(
    task_id: str, timeout: int = 300, check_interval: float = 0.5
) -> Tuple[bool, Optional[str]]:
    """
    Wait for task to complete.
    
    Args:
        task_id: Task identifier
        timeout: Maximum wait time in seconds
        check_interval: How often to check status
        
    Returns:
        Tuple of (is_complete, status)
    """
    import time

    detector = get_completion_detector()
    start_time = time.time()

    while time.time() - start_time < timeout:
        is_complete, status = detector.is_task_complete(task_id)
        if is_complete:
            return True, status

        time.sleep(check_interval)

    return False, "TIMEOUT"




