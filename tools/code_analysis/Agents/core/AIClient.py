import os
import json
import logging
import hashlib
import asyncio
import sys
from typing import Optional, Dict, Any

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import necessary modules
from utils.plugins.LoggerManager import LoggerManager
from utils.plugins.PatchTrackingManager import PatchTrackingManager
from utils.plugins.AIConfidenceManager import AIConfidenceManager
from utils.plugins.AIModelManager import AIModelManager
from utils.plugins.PerformanceMonitor import PerformanceMonitor
from utils.plugins.AgentMemory import AgentMemory
from Agents.core.AgentBase import AgentBase
from Agents.AgentRegistry import AgentRegistry

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Initialize logging
logger = LoggerManager(log_file=os.path.join(LOG_DIR, "ai_client.log")).get_logger()


class AIClient(AgentBase):
    """
    AIClient extends AgentBase to integrate AI-driven debugging, model management, and agent interactions.

    ✅ Supports multiple AI models (Mistral, DeepSeek, OpenAI).
    ✅ Manages AI confidence scores and patch tracking.
    ✅ Uses AI-generated patches for debugging automation.
    ✅ Self-improvement via error tracking and AI patch refinement.
    ✅ Supports scheduled AI-based tasks.
    """

    DEFAULT_MODELS = ["mistral", "deepseek", "openai"]
    MODEL_STORAGE_DIR = "models"

    def __init__(self, name="AIClientAgent", project_name="AI_Debugger_Assistant"):
        super().__init__(name=name, project_name=project_name)
        self.logger = LoggerManager(log_file=os.path.join(LOG_DIR, f"{self.name}.log")).get_logger()
        self.logger.info(f"🚀 {self.name} initialized for project '{project_name}'.")

        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.patch_tracker = PatchTrackingManager()
        self.confidence_manager = AIConfidenceManager()
        self.model_manager = AIModelManager()
        self.performance_monitor = PerformanceMonitor()
        self.memory_manager = AgentMemory()

        self.model_priority = self.DEFAULT_MODELS  # Default AI model selection priority
        os.makedirs(self.MODEL_STORAGE_DIR, exist_ok=True)  # Ensure model storage exists

        # Register periodic self-improvement task (runs every 6 hours)
        self.scheduler.add_job(self.self_improve, "interval", hours=6)
        self.logger.info("🛠️ AIClient self-improvement task scheduled.")

    async def solve_task(self, task_data: Dict[str, Any]) -> str:
        """
        Processes AI debugging and model execution tasks.
        Supports:
          - Patch generation
          - Patch refinement
          - AI confidence evaluations
        """
        task_type = task_data.get("task_type", "unknown")
        error_msg = task_data.get("error_msg", "")
        code_context = task_data.get("code_context", "")
        test_file = task_data.get("test_file", "")

        if task_type == "generate_patch":
            return self.generate_patch(error_msg, code_context, test_file)

        elif task_type == "refine_patch":
            patch = task_data.get("patch", "")
            return self.refine_patch(patch)

        return "❌ Unknown task type."

    def generate_patch(self, error_msg: str, code_context: str, test_file: str) -> Optional[str]:
        """
        Generates an AI patch using the best available model, tracks confidence, and refines if needed.
        """
        request_prompt = self._format_prompt(error_msg, code_context, test_file)
        error_signature = self._compute_error_signature(error_msg, code_context)

        past_confidence = self.confidence_manager.get_best_high_confidence_patch(error_signature) or 0

        for model in self.model_priority:
            patch = self.model_manager.generate_with_model(model, request_prompt)
            if patch:
                confidence_score, reason = self.confidence_manager.assign_confidence_score(error_signature, patch)

                if confidence_score > past_confidence:
                    logger.info(f"✅ AI confidence improved ({past_confidence} ➡ {confidence_score}). Patch accepted.")
                    self.confidence_manager.store_patch(error_signature, patch, confidence_score)
                    return patch

        logger.error("❌ No confident patch found.")
        return None

    def refine_patch(self, patch: str) -> Optional[str]:
        """
        Attempts to refine an AI-generated patch by leveraging confidence scoring.
        """
        error_signature = self._compute_error_signature(patch, "")

        for model in self.model_priority:
            refined_patch = self.model_manager.generate_with_model(model, f"Refine this patch:\n{patch}")
            if refined_patch:
                confidence_score, reason = self.confidence_manager.assign_confidence_score(error_signature, refined_patch)

                if confidence_score > 75:
                    logger.info(f"✅ AI successfully refined patch (Confidence: {confidence_score}).")
                    self.confidence_manager.store_patch(error_signature, refined_patch, confidence_score)
                    return refined_patch

        logger.warning("⚠ AI refinement failed.")
        return None

    def _format_prompt(self, error_msg: str, code_context: str, test_file: str) -> str:
        """Formats the debugging request into a structured AI prompt."""
        return (
            f"You are an AI debugging assistant.\n\n"
            f"Test File: {test_file}\n"
            f"Error Message: {error_msg}\n"
            f"Code Context:\n{code_context}\n\n"
            f"Generate a fix in `diff --git` format."
        )

    def _compute_error_signature(self, error_msg: str, code_context: str) -> str:
        """
        Computes a unique hash for error tracking.
        """
        combined = error_msg + code_context
        return hashlib.sha256(combined.encode("utf-8")).hexdigest()

    def self_improve(self):
        """
        Analyzes AI performance data and suggests improvements.
        """
        analysis = self.performance_monitor.analyze_performance(self.name)
        success_rate = analysis.get("success_rate", 0)
        failures = analysis.get("failures", 0)

        if success_rate < 80 and failures > 10:
            logger.warning(f"⚠️ AIClient needs improvement. Success Rate: {success_rate}%")
            reason = max(analysis.get("failure_details", {}), key=analysis["failure_details"].get, default="Unknown")
            self.take_action_based_on_failure(reason)
        else:
            logger.info(f"✅ AIClient performance stable. Success Rate: {success_rate}%")

    def take_action_based_on_failure(self, reason: str):
        """
        Suggests corrective measures based on failure trends.
        """
        suggestions = {
            "communication": "Check network or model service.",
            "permission": "Check file/directory permissions.",
            "timeout": "Increase timeout or optimize queries.",
        }
        suggestion = suggestions.get(reason.lower(), "Review logs for more details.")
        logger.info(f"Suggested improvement: {suggestion}")

    def shutdown(self):
        """
        Shuts down the agent and stops scheduled AI improvements.
        """
        self.scheduler.shutdown()
        logger.info(f"Agent '{self.name}' shutdown complete.")


# =====================================
# ✅ Example Usage (Ensures Task is Awaited)
# =====================================
if __name__ == "__main__":
    client = AIClient()
    registry = AgentRegistry()
    registry.register_agent("ai_client", client)

    async def run_example():
        result = await client.solve_task({
            "task_type": "generate_patch",
            "error_msg": "SyntaxError: invalid syntax",
            "code_context": "def my_function():\n    return print('Hello) ",
            "test_file": "example_test.py"
        })
        logger.info(f"Generated Patch:\n{result}")

    asyncio.run(run_example())

    client.shutdown()
