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

<<<<<<< HEAD
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)
=======
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from datetime import datetime
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1


@dataclass
class ContextSession:
    """
<<<<<<< HEAD
    Represents an active context processing session with enhanced validation and methods.
=======
    Represents an active context processing session.
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

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
<<<<<<< HEAD
    context_data: Dict[str, Any] = field(default_factory=dict)
    risk_metrics: Optional[Any] = None  # RiskMetrics from risk_calculator_service.py
    ai_suggestions: List[Dict[str, Any]] = field(default_factory=list)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    status: str = "active"  # 'active', 'paused', 'completed', 'error'
    metadata: Dict[str, Any] = field(default_factory=dict)
    session_tags: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Initialize and validate session data."""
        # Auto-generate session_id if not provided
        if not self.session_id:
            self.session_id = f"{self.user_id}_{self.context_type}_{int(datetime.now().timestamp())}"

        # Validate required fields
        if not self.user_id:
            raise ValueError("user_id is required for ContextSession")

        if not self.context_type:
            raise ValueError("context_type is required for ContextSession")

        # Validate context_type
        valid_types = ['trading', 'collaboration', 'analysis', 'risk', 'ux']
        if self.context_type not in valid_types:
            logger.warning(f"Unknown context_type '{self.context_type}', defaulting to 'analysis'")
            self.context_type = 'analysis'

        # Ensure timestamps are datetime objects
        if isinstance(self.start_time, str):
            try:
                self.start_time = datetime.fromisoformat(self.start_time)
            except ValueError:
                self.start_time = datetime.now()

        if isinstance(self.last_activity, str):
            try:
                self.last_activity = datetime.fromisoformat(self.last_activity)
            except ValueError:
                self.last_activity = datetime.now()

        # Initialize performance tracking
        self.performance_metrics.update({
            'suggestions_generated': 0,
            'suggestions_applied': 0,
            'processing_time_total': 0.0,
            'error_count': 0,
            'last_updated': datetime.now().isoformat()
        })

        logger.info(f"Initialized ContextSession {self.session_id} for user {self.user_id}")

    def update_activity(self):
        """Update the last activity timestamp."""
        self.last_activity = datetime.now()
        self.performance_metrics['last_updated'] = self.last_activity.isoformat()

    def add_suggestion(self, suggestion: 'ContextSuggestion'):
        """Add a validated suggestion to the session."""
        if not isinstance(suggestion, ContextSuggestion):
            logger.error("Attempted to add invalid suggestion type")
            return False

        suggestion_dict = {
            'suggestion_id': suggestion.suggestion_id,
            'session_id': suggestion.session_id,
            'type': suggestion.suggestion_type,
            'confidence': suggestion.confidence_score,
            'content': suggestion.content,
            'reasoning': suggestion.reasoning,
            'timestamp': suggestion.timestamp.isoformat() if isinstance(suggestion.timestamp, datetime) else suggestion.timestamp,
            'applied': suggestion.applied
        }

        self.ai_suggestions.append(suggestion_dict)
        self.performance_metrics['suggestions_generated'] += 1
        self.update_activity()
        return True

    def apply_suggestion(self, suggestion_id: str) -> bool:
        """Mark a suggestion as applied."""
        for suggestion in self.ai_suggestions:
            if suggestion.get('suggestion_id') == suggestion_id:
                suggestion['applied'] = True
                self.performance_metrics['suggestions_applied'] += 1
                self.update_activity()
                return True
        return False

    def record_error(self, error_type: str, error_message: str):
        """Record an error in the session."""
        self.performance_metrics['error_count'] += 1
        error_record = {
            'timestamp': datetime.now().isoformat(),
            'type': error_type,
            'message': error_message
        }

        if 'errors' not in self.metadata:
            self.metadata['errors'] = []
        self.metadata['errors'].append(error_record)
        self.update_activity()

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the session state."""
        duration = (datetime.now() - self.start_time).total_seconds()
        applied_count = sum(1 for s in self.ai_suggestions if s.get('applied', False))

        return {
            'session_id': self.session_id,
            'user_id': self.user_id,
            'context_type': self.context_type,
            'status': self.status,
            'duration_seconds': duration,
            'suggestions_total': len(self.ai_suggestions),
            'suggestions_applied': applied_count,
            'error_count': self.performance_metrics.get('error_count', 0),
            'last_activity': self.last_activity.isoformat(),
            'tags': self.session_tags
        }

    def is_expired(self, max_age_seconds: int = 3600) -> bool:
        """Check if the session has expired due to inactivity."""
        age = (datetime.now() - self.last_activity).total_seconds()
        return age > max_age_seconds
=======
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
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1


@dataclass
class ContextSuggestion:
    """
<<<<<<< HEAD
    AI-generated context-aware suggestion with enhanced validation and methods.
=======
    AI-generated context-aware suggestion.
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

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
<<<<<<< HEAD
    applied: bool = False
    priority: str = "normal"  # 'low', 'normal', 'high', 'urgent'
    category: str = "general"  # 'risk', 'trading', 'collaboration', 'analysis'
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate and initialize suggestion data."""
        # Auto-generate suggestion_id if not provided
        if not self.suggestion_id:
            self.suggestion_id = f"{self.session_id}_{self.suggestion_type}_{int(datetime.now().timestamp())}"

        # Validate required fields
        if not self.session_id:
            raise ValueError("session_id is required for ContextSuggestion")

        if not self.suggestion_type:
            raise ValueError("suggestion_type is required for ContextSuggestion")

        # Validate suggestion_type
        valid_types = ['risk_alert', 'optimization', 'insight', 'action', 'warning', 'opportunity']
        if self.suggestion_type not in valid_types:
            logger.warning(f"Unknown suggestion_type '{self.suggestion_type}', keeping as-is")

        # Validate confidence_score
        if not isinstance(self.confidence_score, (int, float)) or not (0 <= self.confidence_score <= 1):
            logger.warning(f"Invalid confidence_score {self.confidence_score}, setting to 0.5")
            self.confidence_score = 0.5

        # Validate priority
        valid_priorities = ['low', 'normal', 'high', 'urgent']
        if self.priority not in valid_priorities:
            self.priority = "normal"

        # Ensure timestamp is datetime
        if isinstance(self.timestamp, str):
            try:
                self.timestamp = datetime.fromisoformat(self.timestamp)
            except ValueError:
                self.timestamp = datetime.now()

        # Validate content
        if not isinstance(self.content, dict):
            logger.warning("Invalid content format, converting to dict")
            self.content = {'message': str(self.content)}

    def mark_applied(self):
        """Mark the suggestion as applied."""
        self.applied = True
        self.metadata['applied_at'] = datetime.now().isoformat()

    def get_priority_score(self) -> int:
        """Get numerical priority score for sorting."""
        priority_map = {'low': 1, 'normal': 2, 'high': 3, 'urgent': 4}
        return priority_map.get(self.priority, 2)

    def to_dict(self) -> Dict[str, Any]:
        """Convert suggestion to dictionary for serialization."""
        data = {
            'suggestion_id': self.suggestion_id,
            'session_id': self.session_id,
            'type': self.suggestion_type,
            'confidence': self.confidence_score,
            'content': self.content,
            'reasoning': self.reasoning,
            'timestamp': self.timestamp.isoformat(),
            'applied': self.applied,
            'priority': self.priority,
            'category': self.category,
            'metadata': self.metadata
        }
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextSuggestion':
        """Create suggestion from dictionary."""
        # Handle timestamp conversion
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp)
            except ValueError:
                timestamp = datetime.now()
        elif not isinstance(timestamp, datetime):
            timestamp = datetime.now()

        return cls(
            suggestion_id=data.get('suggestion_id', ''),
            session_id=data.get('session_id', ''),
            suggestion_type=data.get('type', 'insight'),
            confidence_score=data.get('confidence', 0.5),
            content=data.get('content', {}),
            reasoning=data.get('reasoning', ''),
            timestamp=timestamp,
            applied=data.get('applied', False),
            priority=data.get('priority', 'normal'),
            category=data.get('category', 'general'),
            metadata=data.get('metadata', {})
        )

    def is_relevant(self, context_age_seconds: int = 300) -> bool:
        """Check if suggestion is still relevant based on age."""
        age = (datetime.now() - self.timestamp).total_seconds()
        return age <= context_age_seconds

    def get_actionable_content(self) -> Dict[str, Any]:
        """Get the actionable parts of the suggestion content."""
        actionable = {
            'action': self.content.get('action', 'review'),
            'priority': self.priority,
            'confidence': self.confidence_score
        }

        # Add specific actionable items based on suggestion type
        if self.suggestion_type == 'risk_alert':
            actionable.update({
                'risk_level': self.content.get('risk_level', 'medium'),
                'recommended_action': self.content.get('suggestion', 'Review risk position')
            })
        elif self.suggestion_type == 'optimization':
            actionable.update({
                'optimization_type': self.content.get('type', 'general'),
                'expected_benefit': self.content.get('benefit', 'Improved performance')
            })

        return actionable


# Utility functions for session management
def create_session(user_id: str, context_type: str, initial_context: Optional[Dict[str, Any]] = None) -> ContextSession:
    """
    Factory function to create a new context session with validation.

    Args:
        user_id: User identifier
        context_type: Type of context ('trading', 'collaboration', 'analysis', 'risk')
        initial_context: Optional initial context data

    Returns:
        New ContextSession instance
    """
    return ContextSession(
        session_id="",  # Will be auto-generated
        user_id=user_id,
        context_type=context_type,
        start_time=datetime.now(),
        last_activity=datetime.now(),
        context_data=initial_context or {}
    )


def create_suggestion(session_id: str, suggestion_type: str, content: Dict[str, Any],
                     reasoning: str, confidence: float = 0.8, priority: str = "normal") -> ContextSuggestion:
    """
    Factory function to create a new context suggestion with validation.

    Args:
        session_id: Session identifier
        suggestion_type: Type of suggestion
        content: Suggestion content
        reasoning: Reasoning for the suggestion
        confidence: Confidence score (0-1)
        priority: Priority level

    Returns:
        New ContextSuggestion instance
    """
    return ContextSuggestion(
        suggestion_id="",  # Will be auto-generated
        session_id=session_id,
        suggestion_type=suggestion_type,
        confidence_score=confidence,
        content=content,
        reasoning=reasoning,
        timestamp=datetime.now(),
        priority=priority
    )


def validate_session_data(session: ContextSession) -> List[str]:
    """
    Validate session data and return list of validation errors.

    Args:
        session: Session to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    if not session.session_id:
        errors.append("Session ID is required")

    if not session.user_id:
        errors.append("User ID is required")

    if session.context_type not in ['trading', 'collaboration', 'analysis', 'risk', 'ux']:
        errors.append(f"Invalid context type: {session.context_type}")

    if not isinstance(session.context_data, dict):
        errors.append("Context data must be a dictionary")

    if len(session.ai_suggestions) > 1000:
        errors.append("Too many suggestions in session (max 1000)")

    return errors


def validate_suggestion_data(suggestion: ContextSuggestion) -> List[str]:
    """
    Validate suggestion data and return list of validation errors.

    Args:
        suggestion: Suggestion to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    if not suggestion.suggestion_id:
        errors.append("Suggestion ID is required")

    if not suggestion.session_id:
        errors.append("Session ID is required")

    if suggestion.suggestion_type not in ['risk_alert', 'optimization', 'insight', 'action', 'warning', 'opportunity']:
        errors.append(f"Invalid suggestion type: {suggestion.suggestion_type}")

    if not isinstance(suggestion.confidence_score, (int, float)) or not (0 <= suggestion.confidence_score <= 1):
        errors.append(f"Invalid confidence score: {suggestion.confidence_score}")

    if not isinstance(suggestion.content, dict):
        errors.append("Content must be a dictionary")

    if not suggestion.reasoning:
        errors.append("Reasoning is required")

    return errors
=======
    applied: bool = False
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
