"""
<!-- SSOT Domain: core -->

GPT Integration for Workflows - V2 Compliant
============================================

Integrates AutomationEngine (OpenAI API) into workflow system.
Enables GPT-powered workflow steps with direct API calls.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

import logging
from typing import Any, Optional

# V2 Integration
try:
    from ..ai_automation.automation_engine import AutomationEngine
    from ..core.config_ssot import get_unified_config
    from ..core.unified_logging_system import get_logger
    AUTOMATION_ENGINE_AVAILABLE = True
except ImportError as e:
    AUTOMATION_ENGINE_AVAILABLE = False
    logging.warning(f"AutomationEngine not available: {e}")

    def get_unified_config():
        return type("MockConfig", (), {"get_env": lambda x, y=None: y})()

    def get_logger(name):
        return logging.getLogger(name)

    AutomationEngine = None

from .models import AIResponse, ResponseType, WorkflowStep


class GPTWorkflowIntegration:
    """
    Integration layer for GPT API automation in workflows.
    
    Provides GPT-powered workflow steps using AutomationEngine
    for direct OpenAI API calls within workflow execution.
    """

    def __init__(self, config: Optional[dict[str, Any]] = None):
        """
        Initialize GPT workflow integration.
        
        Args:
            config: Configuration dictionary with GPT settings
        """
        self.config = config or {}
        self.logger = get_logger(__name__)
        self.unified_config = get_unified_config()
        
        # GPT settings from config
        gpt_config = self.config.get("gpt", {})
        self.default_model = gpt_config.get("model", "gpt-3.5-turbo")
        self.default_timeout = gpt_config.get("timeout", 15.0)
        self.default_max_retries = gpt_config.get("max_retries", 2)
        
        # Initialize AutomationEngine if available
        self.engine: Optional[AutomationEngine] = None
        if AUTOMATION_ENGINE_AVAILABLE and AutomationEngine:
            try:
                self.engine = AutomationEngine(
                    model=self.default_model,
                    max_retries=self.default_max_retries,
                    timeout_seconds=self.default_timeout,
                )
                self.logger.info("GPT Workflow Integration initialized")
            except Exception as e:
                self.logger.warning(f"Failed to initialize AutomationEngine: {e}")
                self.engine = None

    def is_available(self) -> bool:
        """Check if GPT integration is available."""
        return AUTOMATION_ENGINE_AVAILABLE and self.engine is not None

    def execute_gpt_step(
        self, step: WorkflowStep, workflow_data: Optional[dict[str, Any]] = None
    ) -> AIResponse:
        """
        Execute a workflow step using GPT API.
        
        Args:
            step: Workflow step to execute
            workflow_data: Optional workflow context data
            
        Returns:
            AIResponse with GPT result
            
        Raises:
            RuntimeError: If AutomationEngine is not available
        """
        if not self.is_available():
            raise RuntimeError(
                "AutomationEngine not available. "
                "Install openai package and set OPENAI_API_KEY."
            )

        # Format prompt with workflow data if provided
        prompt = step.prompt_template
        if workflow_data:
            try:
                prompt = prompt.format(**workflow_data)
            except KeyError:
                self.logger.warning(
                    f"Could not format prompt with workflow_data, using template as-is"
                )

        self.logger.info(f"Executing GPT step: {step.name}")
        self.logger.debug(f"Prompt: {prompt[:100]}...")

        try:
            # Execute GPT call
            response_text = self.engine.run_prompt(prompt)
            
            # Create AIResponse (using correct model structure)
            import time
            response = AIResponse(
                agent="GPT_API",
                text=response_text,
                timestamp=time.time(),
                message_id=f"gpt_{step.id}_{int(time.time())}",
                response_type=step.expected_response_type,
                metadata={
                    "model": self.engine.model,
                    "step_name": step.name,
                    "gpt_api_call": True,
                },
            )

            self.logger.info(f"GPT step completed: {step.name}")
            return response

        except Exception as e:
            self.logger.error(f"GPT step failed: {step.name} - {e}")
            # Return error response
            import time
            return AIResponse(
                agent="GPT_API",
                text=f"GPT API call failed: {str(e)}",
                timestamp=time.time(),
                message_id=f"gpt_error_{step.id}_{int(time.time())}",
                response_type=step.expected_response_type,
                metadata={
                    "error": True,
                    "error_message": str(e),
                    "step_name": step.name,
                },
            )

    def create_gpt_step_builder(self):
        """
        Create a builder for GPT-powered workflow steps.
        
        Returns:
            GPTStepBuilder instance
        """
        return GPTStepBuilder(self)


class GPTStepBuilder:
    """
    Builder for creating GPT-powered workflow steps.
    
    Provides convenient methods for creating workflow steps
    that use GPT API for execution.
    """

    def __init__(self, integration: GPTWorkflowIntegration):
        """
        Initialize GPT step builder.
        
        Args:
            integration: GPTWorkflowIntegration instance
        """
        self.integration = integration
        self.steps: list[WorkflowStep] = []
        self.step_counter = 0

    def create_gpt_step(
        self,
        name: str,
        description: str,
        prompt: str,
        response_type: ResponseType = ResponseType.DECISION_ANALYSIS,
        timeout_seconds: int = 300,
        dependencies: Optional[list[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> WorkflowStep:
        """
        Create a GPT-powered workflow step.
        
        Args:
            name: Step name
            description: Step description
            prompt: GPT prompt template (supports {variable} formatting)
            response_type: Expected response type
            timeout_seconds: Step timeout
            dependencies: Step dependencies
            metadata: Additional metadata
            
        Returns:
            WorkflowStep configured for GPT execution
        """
        step_id = f"gpt_step_{self.step_counter}"
        self.step_counter += 1

        step = WorkflowStep(
            id=step_id,
            name=name,
            description=description,
            agent_target="GPT_API",  # Special target for GPT steps
            prompt_template=prompt,
            expected_response_type=response_type,
            timeout_seconds=timeout_seconds,
            dependencies=dependencies or [],
            metadata={
                **(metadata or {}),
                "gpt_enabled": True,
                "execution_type": "gpt_api",
            },
        )

        self.steps.append(step)
        return step

    def get_steps(self) -> list[WorkflowStep]:
        """Get all created GPT steps."""
        return self.steps.copy()


# Global instance for easy access
_gpt_integration: Optional[GPTWorkflowIntegration] = None


def get_gpt_integration(config: Optional[dict[str, Any]] = None) -> GPTWorkflowIntegration:
    """
    Get or create global GPT workflow integration instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        GPTWorkflowIntegration instance
    """
    global _gpt_integration
    if _gpt_integration is None:
        _gpt_integration = GPTWorkflowIntegration(config)
    return _gpt_integration

