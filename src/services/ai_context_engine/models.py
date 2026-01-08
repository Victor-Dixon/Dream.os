#!/usr/bin/env python3
"""
AI Context Engine Data Models
=============================

Data models and dataclasses for the AI Context Engine.

<!-- SSOT Domain: ai_context -->

Navigation References:
├── Related Files:
│   ├── Main Engine → ai_context_engine.py
│   ├── Session Manager → session_manager.py
│   └── Context Processors → context_processors.py
├── Documentation:
│   └── Phase 5 Architecture → docs/PHASE5_AI_CONTEXT_ENGINE.md
└── Testing:
    └── Integration Tests → tests/integration/test_ai_context_engine.py

Classes:
- ContextSession: Represents an active context processing session
- ContextSuggestion: AI-generated context-aware suggestion
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime


@dataclass
class ContextSession:
    """
    Represents an active context processing session.

    Navigation:
    ├── Used by: SessionManager, ContextProcessors, AIContextEngine
    ├── Related: ContextSuggestion, RiskMetrics (from risk_calculator_service.py)
    └── Documentation: docs/PHASE5_AI_CONTEXT_ENGINE.md#session-management
    """
    session_id: str
    user_id: str
    context_type: str  # 'trading', 'collaboration', 'analysis', 'risk'
    start_time: datetime
    last_activity: datetime
    context_data: Dict[str, Any]
    risk_metrics: Optional[Any] = None  # RiskMetrics from risk_calculator_service.py
    ai_suggestions: List[Dict[str, Any]] = None
    performance_metrics: Dict[str, float] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.ai_suggestions is None:
            self.ai_suggestions = []
        if self.performance_metrics is None:
            self.performance_metrics = {}


@dataclass
class ContextSuggestion:
    """
    AI-generated context-aware suggestion.

    Navigation:
    ├── Used by: SuggestionGenerators, ContextProcessors, AIContextEngine
    ├── Related: ContextSession
    └── Documentation: docs/PHASE5_AI_CONTEXT_ENGINE.md#ai-suggestions
    """
    suggestion_id: str
    session_id: str
    suggestion_type: str  # 'risk_alert', 'optimization', 'insight', 'action'
    confidence_score: float
    content: Dict[str, Any]
    reasoning: str
    timestamp: datetime
    applied: bool = False