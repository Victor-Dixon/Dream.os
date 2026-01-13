"""Modular template engine wrapper."""
from systems.templates.templates.engine.template_engine import PromptTemplateEngine as _Engine

class TemplateEngine(_Engine):
    """Backward-compatible wrapper for the consolidated template engine."""
    pass

__all__ = ["TemplateEngine"]
