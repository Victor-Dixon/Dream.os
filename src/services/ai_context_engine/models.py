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

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional



@dataclass
class ContextSession:
    """


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
    context_data: Dict[str, Any] = field(default_factory=dict)
    ai_suggestions: list["ContextSuggestion"] = field(default_factory=list)
    risk_metrics: Optional[Any] = None



@dataclass
class ContextSuggestion:
    """


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
