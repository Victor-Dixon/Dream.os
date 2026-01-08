#!/usr/bin/env python3
"""
AI Context Engine Package
========================

V2 Compliant modular AI context processing system.

<!-- SSOT Domain: ai_context -->

This package provides:
- AIContextEngine: Main context processing engine
- ContextSession & ContextSuggestion: Data models
- ContextProcessor subclasses: Specialized context processing
- SessionManager: Session lifecycle management
- SuggestionGenerators: AI-powered suggestion generation

Navigation:
├── Main Engine → ai_context_engine.py
├── Data Models → models.py
├── Context Processing → context_processors.py
├── Session Management → session_manager.py
├── Suggestion Generation → suggestion_generators.py
└── Testing → ../../tests/integration/test_ai_context_engine.py
"""

from .ai_context_engine import AIContextEngine, ai_context_engine
from .models import ContextSession, ContextSuggestion
from .context_processors import (
    ContextProcessor, TradingContextProcessor, CollaborationContextProcessor,
    AnalysisContextProcessor, RiskContextProcessor
)
from .session_manager import SessionManager
from .suggestion_generators import SuggestionGenerators

__all__ = [
    'AIContextEngine',
    'ai_context_engine',
    'ContextSession',
    'ContextSuggestion',
    'ContextProcessor',
    'TradingContextProcessor',
    'CollaborationContextProcessor',
    'AnalysisContextProcessor',
    'RiskContextProcessor',
    'SessionManager',
    'SuggestionGenerators'
]