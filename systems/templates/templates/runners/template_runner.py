"""Unified template runner module."""
from systems.templates.templates.runners.template_runner import PromptOrchestrator as _Runner

class TemplateRunner(_Runner):
    """Wrapper exposing the prompt orchestrator as a template runner."""
    pass

__all__ = ["TemplateRunner"]
