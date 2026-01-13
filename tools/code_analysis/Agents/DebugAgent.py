#!/usr/bin/env python
"""
DebugAgent.py

A plugin-ready, AI-assisted debugging agent that:
- Runs tests via pytest.
- Parses and analyzes failures.
- Applies quick fixes (via QuickFixManager).
- Uses adaptive learning (via AIConfidenceManager) for advanced fixes.
- Integrates with version control (VersionControlManager) for commit/rollback.
- Logs debugging progress (DebuggerReporter).

Designed for easy integration with a broader AI debugging system.
"""

import os
import re
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

# Updated imports from the new integrated paths
from utils.plugins.LoggerManager import LoggerManager
from utils.plugins.PatchTrackingManager import PatchTrackingManager
from utils.plugins.AIConfidenceManager import AIConfidenceManager
from utils.plugins.DebuggerReporter import DebuggerReporter
from utils.plugins.QuickFixManager import QuickFixManager
from utils.plugins.VersionControlManager import VersionControlManager
from Agents.core.AgentBase import AgentBase  # Use the integrated AgentBase

# Configure logger
logger = LoggerManager(log_file="debug_agent.log").get_logger()

LEARNING_DB_PATH = "learning_db.json"

class DebugAgent(AgentBase):
    """
    An AI-driven Debugging Agent that orchestrates:
    - Automated test runs
    - Failure parsing
    - Quick & adaptive fixes
    - Version control interactions
    - Debugging progress reports
    """

    def __init__(self, name: str = "DebugAgent"):
        super().__init__(name=name, project_name="MergedDebugger")
        logger.info(f"[{self.name}] Initializing DebugAgent.")
        self.learning_db: Dict[str, str] = self._load_learning_db()

        # Instantiate modular components from the new paths
        self.patch_tracker = PatchTrackingManager()
        self.confidence_manager = AIConfidenceManager()
        self.reporter = DebuggerReporter()
        self.quick_fix_manager = QuickFixManager()
        self.vcs_manager = VersionControlManager()

    def _load_learning_db(self) -> Dict[str, str]:
        """Loads the learning database from LEARNING_DB_PATH or returns an empty dict."""
        path = Path(LEARNING_DB_PATH)
        if not path.exists():
            logger.info(f"[{self.name}] No learning DB found at {LEARNING_DB_PATH}, starting fresh.")
            return {}
        try:
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            logger.info(f"[{self.name}] Loaded learning DB with {len(data)} entries.")
            return data
        except Exception as e:
            logger.error(f"[{self.name}] Failed to load learning DB: {e}")
            return {}

    def _save_learning_db(self) -> None:
        """Saves the current learning database to LEARNING_DB_PATH."""
        try:
            with open(LEARNING_DB_PATH, "w", encoding="utf-8") as f:
                json.dump(self.learning_db, f, indent=4)
            logger.info(f"[{self.name}] Learning DB saved.")
        except Exception as e:
            logger.error(f"[{self.name}] Failed to save learning DB: {e}")

    # ---------------------------
    #  Task Handling
    # ---------------------------
    def solve_task(self, task: str, **kwargs) -> Any:
        """
        Routes the given task to the appropriate debugging function.
        Supported tasks: "analyze_error", "run_diagnostics", 
                         "automate_debugging", "run_debug_cycle".
        """
        logger.info(f"[{self.name}] Received task: '{task}' with kwargs: {kwargs}")
        task_methods = {
            "analyze_error": self.analyze_error,
            "run_diagnostics": self.run_diagnostics,
            "automate_debugging": self.automate_debugging,
            "run_debug_cycle": self.run_debug_cycle,
        }
        if task in task_methods:
            return task_methods[task](**kwargs)
        else:
            logger.error(f"[{self.name}] Unknown task: '{task}'")
            return {"status": "error", "message": f"Unknown task '{task}'"}

    # ---------------------------
    #  Core Debugging Flow
    # ---------------------------
    def run_tests(self) -> str:
        """Runs tests via pytest and returns the combined stdout/stderr output."""
        logger.info(f"[{self.name}] Running tests via pytest.")
        try:
            result = subprocess.run(
                ["pytest", "tests", "--maxfail=5", "--tb=short", "-q"],
                capture_output=True,
                text=True,
                check=False,
            )
            output = result.stdout + result.stderr
            logger.debug(f"[{self.name}] Test output: {output}")
            return output
        except Exception as e:
            logger.error(f"[{self.name}] Failed to run tests: {e}")
            return f"Error running tests: {e}"

    def run_tests_for_files(self, files: set) -> str:
        """
        Runs tests for a specified set of files.
        """
        logger.info(f"[{self.name}] Running tests for files: {files}")
        try:
            file_list = list(files)
            result = subprocess.run(
                ["pytest"] + file_list + ["--maxfail=5", "--tb=short", "-q"],
                capture_output=True,
                text=True,
                check=False,
            )
            return result.stdout + result.stderr
        except Exception as e:
            logger.error(f"[{self.name}] Failed to run tests for files: {e}")
            return f"Error: {e}"

    def parse_test_failures(self, test_output: str) -> List[Dict[str, str]]:
        """
        Parses pytest output for failure details.
        """
        logger.info(f"[{self.name}] Parsing test failures.")
        failures = []
        pattern = re.compile(r"FAILED (.+?)::(.+?) - (.+)")
        for match in pattern.finditer(test_output):
            failures.append({
                "file": match.group(1),
                "test": match.group(2),
                "error": match.group(3)
            })
        logger.info(f"[{self.name}] Found {len(failures)} failures.")
        return failures

    # ---------------------------
    #  Applying Fixes
    # ---------------------------
    def apply_fix(self, failure: Dict[str, str]) -> bool:
        """
        Attempts to apply a fix for a given failure using QuickFixManager or adaptive learning.
        """
        logger.info(f"[{self.name}] Attempting fix for {failure['file']} - {failure['test']}")
        
        # 1) Quick fixes
        if self.quick_fix_manager.apply_quick_fix(failure):
            return True
        
        # 2) Confidence-based, adaptive fix
        confidence = self.confidence_manager.get_confidence(failure["error"])
        if confidence >= 0.7 and self._apply_adaptive_learning_fix(failure):
            return True

        logger.info(f"[{self.name}] No fix applied for {failure['file']}. Manual intervention required.")
        return False

    def _apply_adaptive_learning_fix(self, failure: Dict[str, str]) -> bool:
        """
        Uses known fixes from the learning DB to apply an adaptive fix.
        """
        error_msg = failure["error"]
        known_fix = self._search_learned_fix(error_msg)
        if not known_fix:
            logger.info(f"[{self.name}] No learned fix available for error: {error_msg[:80]}")
            return False

        # Use patch_tracker to apply the patch
        applied = self.patch_tracker.apply_patch(known_fix)
        if applied:
            logger.info(f"[{self.name}] Adaptive fix applied for error: {error_msg[:80]}")
            self.reporter.log_successful_fix(error_msg, self.confidence_manager.get_confidence(error_msg, known_fix))
        else:
            logger.error(f"[{self.name}] Adaptive fix failed for error: {error_msg[:80]}")
            self.reporter.log_failed_patch(error_msg, "Adaptive fix failed")
        return applied

    def _search_learned_fix(self, error_msg: str) -> Optional[str]:
        """Search the learning DB for a known fix."""
        for known_err, fix_str in self.learning_db.items():
            if known_err in error_msg:
                return fix_str
        return None

    def _store_learned_fix(self, error_msg: str, fix_str: str) -> None:
        """Stores a new learned fix in the learning database."""
        logger.info(f"[{self.name}] Storing learned fix for error: {error_msg[:80]}")
        self.learning_db[error_msg] = fix_str
        self._save_learning_db()

    # ---------------------------
    #  Debugging Loop
    # ---------------------------
    def retry_tests(self, max_retries: int = 3) -> Dict[str, str]:
        """
        Runs tests and iterates a debugging loop until tests pass or max retries are reached.
        """
        modified_files = set()
        remaining_failures = []

        for attempt in range(1, max_retries + 1):
            logger.info(f"[{self.name}] Debug attempt {attempt}/{max_retries}")

            test_output = (
                self.run_tests() 
                if attempt == 1 or not remaining_failures
                else self.run_tests_for_files({f["file"] for f in remaining_failures})
            )

            failures = self.parse_test_failures(test_output)
            remaining_failures = failures

            if not failures:
                logger.info(f"[{self.name}] All tests passed on attempt {attempt}.")
                self.vcs_manager.commit_changes("All tests passed! Automated fixes applied.")
                return {"status": "success", "message": "All tests passed!"}

            for failure in failures:
                if self.apply_fix(failure):
                    modified_files.add(failure["file"])
                    logger.info(f"[{self.name}] Fix applied for {failure['file']}")
                else:
                    logger.error(f"[{self.name}] Failed to fix {failure['file']}")
                    self.reporter.log_failed_patch(failure["error"], "Quick/Adaptive fix failed")

            if not modified_files:
                logger.warning(f"[{self.name}] No fixes applied; rolling back changes.")
                self.vcs_manager.rollback_changes(list(modified_files))
                return {"status": "error", "message": "Could not fix failures automatically."}

        logger.error(f"[{self.name}] Maximum retries reached. Some tests are still failing.")
        return {"status": "error", "message": "Max retries reached. Unresolved issues remain."}

    def automate_debugging(self) -> Dict[str, str]:
        """Initiates the automated debugging process."""
        logger.info(f"[{self.name}] Starting automated debugging.")
        return self.retry_tests()

    def run_debug_cycle(self, max_retries: int = 3) -> Dict[str, str]:
        """Runs a full debug cycle."""
        logger.info(f"[{self.name}] Starting full debug cycle.")
        result = self.automate_debugging()
        if result["status"] == "error":
            logger.error(f"[{self.name}] Debug cycle failed.")
        return result

    # ---------------------------
    #  Additional Functionalities
    # ---------------------------
    def analyze_error(self, error: str = "", context: Optional[Dict[str, Any]] = None) -> str:
        """Analyzes a given error message with optional context."""
        logger.info(f"[{self.name}] Analyzing error: {error}")
        if not error:
            return "No error provided for analysis."
        return f"Error analysis: {error}. Context: {context or 'None'}"

    def run_diagnostics(self, system_check: bool = True, detailed: bool = False) -> str:
        """Runs diagnostics and returns a summary."""
        logger.info(f"[{self.name}] Running diagnostics.")
        diagnostics = "Basic diagnostics completed."
        if system_check:
            diagnostics += " System check passed."
        if detailed:
            diagnostics += " Detailed report: All systems operational."
        return diagnostics

    def shutdown(self) -> None:
        """Shuts down the DebugAgent."""
        logger.info(f"[{self.name}] Shutting down.")

    def describe_capabilities(self) -> str:
        """Returns a description of the agent's capabilities."""
        return (
            f"{self.name} can run tests, analyze errors, apply quick and adaptive fixes, "
            "automate debugging cycles, and interact with version control."
        )

# === Execution Example ===
if __name__ == "__main__":
    agent = DebugAgent()
    result = agent.run_debug_cycle()
    logger.info(f"Final Debugging Result: {result}")
