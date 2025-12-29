<!-- SSOT Domain: core -->
"""
Task Completion Detector - SSOT for Detecting Task/Command Completion
======================================================================

Detects when tasks, commands, or processes have completed execution.
Single Source of Truth for all completion detection logic.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-01-27
V2 Compliance: <400 lines
"""

import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class TaskCompletionDetector:
    """
    SSOT for detecting task/command completion.
    
    Detects completion through:
    - Exit codes (0 = success, non-zero = failure)
    - Output patterns (success/failure indicators)
    - Timeout detection (stale tasks)
    - File system changes (output files created)
    - Status file updates
    """

    def __init__(self, timeout_seconds: int = 300):
        """Initialize completion detector."""
        self.timeout_seconds = timeout_seconds
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        self.completion_callbacks: Dict[str, Callable] = {}

    def register_task(
        self,
        task_id: str,
        task_type: str = "command",
        expected_output_file: Optional[str] = None,
        success_patterns: Optional[list[str]] = None,
        failure_patterns: Optional[list[str]] = None,
        timeout: Optional[int] = None,
    ) -> None:
        """
        Register a task for completion monitoring.
        
        Args:
            task_id: Unique task identifier
            task_type: Type of task (command, file_operation, etc.)
            expected_output_file: File that should be created on completion
            success_patterns: List of strings that indicate success
            failure_patterns: List of strings that indicate failure
            timeout: Task-specific timeout (overrides default)
        """
        self.active_tasks[task_id] = {
            "task_id": task_id,
            "task_type": task_type,
            "status": "RUNNING",
            "started_at": datetime.now(),
            "expected_output_file": expected_output_file,
            "success_patterns": success_patterns or [],
            "failure_patterns": failure_patterns or [],
            "timeout": timeout or self.timeout_seconds,
            "last_activity": datetime.now(),
            "output": "",
            "exit_code": None,
        }
        logger.debug(f"✅ Task registered: {task_id} ({task_type})")

    def update_task_output(self, task_id: str, output: str, exit_code: Optional[int] = None) -> bool:
        """
        Update task with output and check for completion.
        
        Args:
            task_id: Task identifier
            output: Output text from task
            exit_code: Exit code (0 = success, non-zero = failure)
            
        Returns:
            True if task is complete, False otherwise
        """
        if task_id not in self.active_tasks:
            logger.warning(f"Task not registered: {task_id}")
            return False

        task = self.active_tasks[task_id]
        task["output"] += output
        task["last_activity"] = datetime.now()

        if exit_code is not None:
            task["exit_code"] = exit_code
            return self._check_completion(task_id, output, exit_code)

        # Check for completion patterns in output
        return self._check_completion(task_id, output, None)

    def _check_completion(self, task_id: str, output: str, exit_code: Optional[int]) -> bool:
        """Check if task has completed based on patterns and exit code."""
        task = self.active_tasks[task_id]

        # Check exit code first (most reliable)
        if exit_code is not None:
            if exit_code == 0:
                task["status"] = "COMPLETED"
                task["completed_at"] = datetime.now()
                self._trigger_completion(task_id, "SUCCESS", f"Exit code: {exit_code}")
                return True
            else:
                task["status"] = "FAILED"
                task["completed_at"] = datetime.now()
                self._trigger_completion(task_id, "FAILED", f"Exit code: {exit_code}")
                return True

        # Check for success patterns
        for pattern in task["success_patterns"]:
            if pattern.lower() in output.lower():
                task["status"] = "COMPLETED"
                task["completed_at"] = datetime.now()
                self._trigger_completion(task_id, "SUCCESS", f"Pattern matched: {pattern}")
                return True

        # Check for failure patterns
        for pattern in task["failure_patterns"]:
            if pattern.lower() in output.lower():
                task["status"] = "FAILED"
                task["completed_at"] = datetime.now()
                self._trigger_completion(task_id, "FAILED", f"Pattern matched: {pattern}")
                return True

        # Check for expected output file
        if task["expected_output_file"]:
            output_path = Path(task["expected_output_file"])
            if output_path.exists():
                # File exists, check if it's recent (within last 5 seconds)
                file_time = datetime.fromtimestamp(output_path.stat().st_mtime)
                if datetime.now() - file_time < timedelta(seconds=5):
                    task["status"] = "COMPLETED"
                    task["completed_at"] = datetime.now()
                    self._trigger_completion(task_id, "SUCCESS", "Output file created")
                    return True

        # Check for timeout
        elapsed = (datetime.now() - task["started_at"]).total_seconds()
        if elapsed > task["timeout"]:
            task["status"] = "TIMEOUT"
            task["completed_at"] = datetime.now()
            self._trigger_completion(task_id, "TIMEOUT", f"Timeout after {elapsed}s")
            return True

        return False

    def _trigger_completion(self, task_id: str, result: str, reason: str) -> None:
        """Trigger completion callback if registered."""
        if task_id in self.completion_callbacks:
            try:
                callback = self.completion_callbacks[task_id]
                callback(task_id, result, reason, self.active_tasks[task_id])
            except Exception as e:
                logger.error(f"Completion callback failed for {task_id}: {e}")

    def is_task_complete(self, task_id: str) -> Tuple[bool, Optional[str]]:
        """
        Check if task is complete.
        
        Returns:
            Tuple of (is_complete, status)
        """
        if task_id not in self.active_tasks:
            return False, None

        task = self.active_tasks[task_id]
        status = task["status"]

        if status in ("COMPLETED", "FAILED", "TIMEOUT"):
            return True, status

        # Check for stale tasks (no activity for 30 seconds)
        if "last_activity" in task:
            elapsed = (datetime.now() - task["last_activity"]).total_seconds()
            if elapsed > 30:
                task["status"] = "STALE"
                task["completed_at"] = datetime.now()
                return True, "STALE"

        return False, status

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get current task status."""
        return self.active_tasks.get(task_id)

    def cleanup_completed_tasks(self, max_age_hours: int = 24) -> int:
        """
        Remove completed tasks older than max_age_hours.
        
        Returns:
            Number of tasks cleaned up
        """
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        to_remove = []

        for task_id, task in self.active_tasks.items():
            if task["status"] in ("COMPLETED", "FAILED", "TIMEOUT", "STALE"):
                completed_at = task.get("completed_at")
                if completed_at and completed_at < cutoff:
                    to_remove.append(task_id)

        for task_id in to_remove:
            del self.active_tasks[task_id]
            if task_id in self.completion_callbacks:
                del self.completion_callbacks[task_id]

        logger.debug(f"Cleaned up {len(to_remove)} completed tasks")
        return len(to_remove)

    def register_completion_callback(
        self, task_id: str, callback: Callable[[str, str, str, Dict], None]
    ) -> None:
        """Register callback to be called when task completes."""
        self.completion_callbacks[task_id] = callback

    def detect_output_completion(
        self, output: str, success_indicators: Optional[list[str]] = None
    ) -> Tuple[bool, Optional[str]]:
        """
        Detect if output indicates completion.
        
        Common completion indicators:
        - Exit code messages
        - "Complete", "Done", "Finished"
        - Error messages
        - Prompt returns (PS>, $, >)
        
        Returns:
            Tuple of (is_complete, reason)
        """
        if not output:
            return False, None

        output_lower = output.lower()

        # Default success indicators
        default_success = [
            "complete",
            "completed",
            "done",
            "finished",
            "success",
            "✅",
            "succeeded",
        ]

        # Default failure indicators
        default_failure = [
            "error",
            "failed",
            "failure",
            "exception",
            "❌",
            "fatal",
            "aborted",
        ]

        # Check for success
        indicators = success_indicators or default_success
        for indicator in indicators:
            if indicator in output_lower:
                return True, f"Success indicator: {indicator}"

        # Check for failure
        for indicator in default_failure:
            if indicator in output_lower:
                return True, f"Failure indicator: {indicator}"

        # Check for prompt return (command completed)
        prompt_patterns = [
            "ps d:\\",
            "ps c:\\",
            "$ ",
            "> ",
            ">>> ",
            "cmd>",
        ]

        # If output ends with prompt, command is complete
        for pattern in prompt_patterns:
            if output.rstrip().endswith(pattern):
                return True, f"Prompt returned: {pattern}"

        # Check for exit code in output
        if "exit code" in output_lower or "exitcode" in output_lower:
            if "0" in output or "success" in output_lower:
                return True, "Exit code 0 detected"
            else:
                return True, "Non-zero exit code detected"

        return False, None


# Global completion detector instance (SSOT)
_completion_detector: Optional[TaskCompletionDetector] = None


def get_completion_detector() -> TaskCompletionDetector:
    """Get global completion detector instance (SSOT)."""
    global _completion_detector
    if _completion_detector is None:
        _completion_detector = TaskCompletionDetector()
    return _completion_detector


def detect_command_completion(output: str) -> Tuple[bool, Optional[str]]:
    """
    Quick helper to detect if command output indicates completion.
    
    Returns:
        Tuple of (is_complete, reason)
    """
    detector = get_completion_detector()
    return detector.detect_output_completion(output)




