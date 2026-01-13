"""Unified template analyzer module."""
from systems.templates.templates.analytics.template_analyzer import UnifiedTemplateAnalyzer as _Analyzer

class TemplateAnalyzer(_Analyzer):
    """Wrapper exposing the unified template analyzer class."""
    pass

__all__ = ["TemplateAnalyzer"]
