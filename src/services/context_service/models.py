#!/usr/bin/env python3
"""
Context Service Data Models - Phase 6 Microservices Architecture
===============================================================

Pydantic models and database schemas for the Context Management Service.

<!-- SSOT Domain: context_service_models -->

Navigation References:
├── Service Implementation → src/services/context_service/main.py
├── Session Manager → src/services/context_service/session_manager.py
├── Database Schema → src/services/context_service/schema.sql

Features:
- ContextSession model with lifecycle management
- UserPreferences for personalization
- ContextEvent for audit trails
- Database table definitions
- Data validation and serialization

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-07
Phase: Phase 6.2 - Microservices Decomposition
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum


class SessionStatus(str, Enum):
    """Enumeration of possible session states."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    EXPIRED = "expired"
    ERROR = "error"


class ContextType(str, Enum):
    """Enumeration of supported context types."""
    TRADING = "trading"
    ANALYSIS = "analysis"
    COLLABORATION = "collaboration"
    LEARNING = "learning"
    GENERAL = "general"


class ContextSession(BaseModel):
    """Model representing a context session."""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: str = Field(..., description="User who owns the session")
    context_type: ContextType = Field(..., description="Type of context session")
    status: SessionStatus = Field(default=SessionStatus.ACTIVE, description="Current session status")
    context_data: Dict[str, Any] = Field(default_factory=dict, description="Session context data")
    user_preferences: Dict[str, Any] = Field(default_factory=dict, description="User preferences for this session")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional session metadata")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.now, description="Session creation timestamp")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last modification timestamp")
    expires_at: Optional[datetime] = Field(default=None, description="Session expiration timestamp")

    # Statistics
    update_count: int = Field(default=0, description="Number of context updates")
    event_count: int = Field(default=0, description="Number of events processed")
    ai_interactions: int = Field(default=0, description="Number of AI interactions")

    @validator('expires_at', pre=True, always=True)
    def set_expires_at(cls, v, values):
        """Set default expiration if not provided."""
        if v is None and 'created_at' in values:
            # Default to 24 hours from creation
            return values['created_at'] + timedelta(hours=24)
        return v

    def is_expired(self) -> bool:
        """Check if session has expired."""
        return datetime.now() > self.expires_at

    def update_timestamp(self):
        """Update the last modified timestamp."""
        self.last_updated = datetime.now()
        self.update_count += 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage."""
        data = self.dict()
        # Convert datetime objects to ISO strings for JSON storage
        data['created_at'] = self.created_at.isoformat()
        data['last_updated'] = self.last_updated.isoformat()
        if self.expires_at:
            data['expires_at'] = self.expires_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextSession':
        """Create from dictionary (e.g., from database)."""
        # Convert ISO strings back to datetime objects
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'last_updated' in data and isinstance(data['last_updated'], str):
            data['last_updated'] = datetime.fromisoformat(data['last_updated'])
        if 'expires_at' in data and isinstance(data['expires_at'], str):
            data['expires_at'] = datetime.fromisoformat(data['expires_at'])
        return cls(**data)


class UserPreferences(BaseModel):
    """Model representing user preferences."""
    user_id: str = Field(..., description="User identifier")
    theme: str = Field(default="auto", description="UI theme preference")
    language: str = Field(default="en", description="Preferred language")
    timezone: str = Field(default="UTC", description="User timezone")
    notifications: Dict[str, bool] = Field(default_factory=lambda: {
        "ai_suggestions": True,
        "context_updates": True,
        "system_alerts": True,
        "performance_reports": False
    }, description="Notification preferences")
    ai_settings: Dict[str, Any] = Field(default_factory=lambda: {
        "suggestion_frequency": "balanced",
        "confidence_threshold": 0.7,
        "max_suggestions_per_session": 10
    }, description="AI interaction preferences")
    privacy_settings: Dict[str, bool] = Field(default_factory=lambda: {
        "analytics_sharing": True,
        "context_logging": True,
        "third_party_integrations": False
    }, description="Privacy and data sharing preferences")

    # Metadata
    created_at: datetime = Field(default_factory=datetime.now, description="Preferences creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

    def update_timestamp(self):
        """Update the last modified timestamp."""
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage."""
        data = self.dict()
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPreferences':
        """Create from dictionary (e.g., from database)."""
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data and isinstance(data['updated_at'], str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)


class ContextEvent(BaseModel):
    """Model representing a context-related event for audit trails."""
    event_id: str = Field(..., description="Unique event identifier")
    session_id: str = Field(..., description="Associated session ID")
    user_id: str = Field(..., description="User who triggered the event")
    event_type: str = Field(..., description="Type of context event")
    event_data: Dict[str, Any] = Field(default_factory=dict, description="Event payload data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Event timestamp")
    correlation_id: Optional[str] = Field(default=None, description="Correlation ID for event tracing")
    source: str = Field(default="context_service", description="Service that generated the event")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for database storage."""
        data = self.dict()
        data['timestamp'] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextEvent':
        """Create from dictionary (e.g., from database)."""
        if 'timestamp' in data and isinstance(data['timestamp'], str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


class SessionStatistics(BaseModel):
    """Model for session performance statistics."""
    session_id: str
    total_updates: int = Field(default=0)
    total_events: int = Field(default=0)
    ai_interactions: int = Field(default=0)
    duration_seconds: float = Field(default=0.0)
    average_response_time: float = Field(default=0.0)
    peak_memory_usage: int = Field(default=0)
    error_count: int = Field(default=0)
    last_activity: datetime = Field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        data = self.dict()
        data['last_activity'] = self.last_activity.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionStatistics':
        """Create from dictionary."""
        if 'last_activity' in data and isinstance(data['last_activity'], str):
            data['last_activity'] = datetime.fromisoformat(data['last_activity'])
        return cls(**data)


# Database schema definitions
CONTEXT_SESSIONS_SCHEMA = """
CREATE TABLE IF NOT EXISTS context_sessions (
    session_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    context_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    context_data JSONB DEFAULT '{}',
    user_preferences JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    update_count INTEGER DEFAULT 0,
    event_count INTEGER DEFAULT 0,
    ai_interactions INTEGER DEFAULT 0,

    -- Indexes for performance
    INDEX idx_user_sessions (user_id, created_at DESC),
    INDEX idx_active_sessions (status, expires_at),
    INDEX idx_context_type (context_type, created_at DESC)
);

-- Partitioning by month for large-scale deployments
-- (Uncomment for production with high session volumes)
-- PARTITION BY RANGE (created_at);
"""

USER_PREFERENCES_SCHEMA = """
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id VARCHAR(255) PRIMARY KEY,
    theme VARCHAR(50) DEFAULT 'auto',
    language VARCHAR(10) DEFAULT 'en',
    timezone VARCHAR(50) DEFAULT 'UTC',
    notifications JSONB DEFAULT '{
        "ai_suggestions": true,
        "context_updates": true,
        "system_alerts": true,
        "performance_reports": false
    }',
    ai_settings JSONB DEFAULT '{
        "suggestion_frequency": "balanced",
        "confidence_threshold": 0.7,
        "max_suggestions_per_session": 10
    }',
    privacy_settings JSONB DEFAULT '{
        "analytics_sharing": true,
        "context_logging": true,
        "third_party_integrations": false
    }',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Indexes
    INDEX idx_user_preferences_updated (updated_at DESC)
);
"""

CONTEXT_EVENTS_SCHEMA = """
CREATE TABLE IF NOT EXISTS context_events (
    event_id VARCHAR(255) PRIMARY KEY,
    session_id VARCHAR(255),
    user_id VARCHAR(255),
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB DEFAULT '{}',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    correlation_id VARCHAR(255),
    source VARCHAR(100) DEFAULT 'context_service',

    -- Indexes for query performance
    INDEX idx_session_events (session_id, timestamp DESC),
    INDEX idx_user_events (user_id, timestamp DESC),
    INDEX idx_event_type (event_type, timestamp DESC),
    INDEX idx_correlation (correlation_id),

    -- Foreign key constraints (optional, depending on data consistency requirements)
    FOREIGN KEY (session_id) REFERENCES context_sessions(session_id) ON DELETE CASCADE
);

-- Retention policy: keep events for 90 days
-- CREATE POLICY events_retention ON context_events
-- USING (timestamp > NOW() - INTERVAL '90 days');
"""

SESSION_STATISTICS_SCHEMA = """
CREATE TABLE IF NOT EXISTS session_statistics (
    session_id VARCHAR(255) PRIMARY KEY,
    total_updates INTEGER DEFAULT 0,
    total_events INTEGER DEFAULT 0,
    ai_interactions INTEGER DEFAULT 0,
    duration_seconds REAL DEFAULT 0.0,
    average_response_time REAL DEFAULT 0.0,
    peak_memory_usage INTEGER DEFAULT 0,
    error_count INTEGER DEFAULT 0,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    -- Foreign key
    FOREIGN KEY (session_id) REFERENCES context_sessions(session_id) ON DELETE CASCADE,

    -- Indexes
    INDEX idx_session_stats_activity (last_activity DESC),
    INDEX idx_session_stats_duration (duration_seconds DESC)
);
"""

# Complete schema creation SQL
CREATE_ALL_TABLES_SQL = [
    CONTEXT_SESSIONS_SCHEMA,
    USER_PREFERENCES_SCHEMA,
    CONTEXT_EVENTS_SCHEMA,
    SESSION_STATISTICS_SCHEMA
]

# Indexes for performance optimization
PERFORMANCE_INDEXES_SQL = """
-- Additional performance indexes
CREATE INDEX IF NOT EXISTS idx_context_sessions_composite
ON context_sessions (user_id, context_type, status, last_updated DESC);

CREATE INDEX IF NOT EXISTS idx_context_events_composite
ON context_events (session_id, event_type, timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_user_preferences_composite
ON user_preferences (updated_at DESC, user_id);

-- Partial indexes for active sessions
CREATE INDEX IF NOT EXISTS idx_active_sessions_only
ON context_sessions (last_updated DESC)
WHERE status = 'active' AND expires_at > NOW();
"""

# Cleanup and maintenance queries
MAINTENANCE_SQL = {
    "cleanup_expired_sessions": """
    UPDATE context_sessions
    SET status = 'expired', last_updated = NOW()
    WHERE status = 'active' AND expires_at < NOW();
    """,

    "archive_old_events": """
    -- Move events older than 90 days to archive table
    INSERT INTO context_events_archive
    SELECT * FROM context_events
    WHERE timestamp < NOW() - INTERVAL '90 days';
    """,

    "cleanup_old_statistics": """
    DELETE FROM session_statistics
    WHERE last_activity < NOW() - INTERVAL '365 days';
    """
}


# Utility functions for data migration and validation
def validate_session_data(session_data: Dict[str, Any]) -> bool:
    """Validate session data structure."""
    required_fields = ['session_id', 'user_id', 'context_type', 'status']
    return all(field in session_data for field in required_fields)


def migrate_legacy_session(legacy_data: Dict[str, Any]) -> ContextSession:
    """Migrate legacy session data to new model."""
    # Handle backward compatibility for older session formats
    session = ContextSession(
        session_id=legacy_data.get('session_id', legacy_data.get('id')),
        user_id=legacy_data['user_id'],
        context_type=legacy_data.get('context_type', 'general'),
        status=legacy_data.get('status', 'active'),
        context_data=legacy_data.get('context_data', {}),
        user_preferences=legacy_data.get('user_preferences', {}),
        metadata=legacy_data.get('metadata', {}),
        created_at=legacy_data.get('created_at', datetime.now()),
        last_updated=legacy_data.get('last_updated', datetime.now()),
        expires_at=legacy_data.get('expires_at'),
        update_count=legacy_data.get('update_count', 0),
        event_count=legacy_data.get('event_count', 0),
        ai_interactions=legacy_data.get('ai_interactions', 0)
    )
    return session


def create_session_from_event(event_data: Dict[str, Any]) -> ContextSession:
    """Create a session from event data (for event-sourced sessions)."""
    return ContextSession(
        session_id=event_data.get('session_id', f"event_{datetime.now().timestamp()}"),
        user_id=event_data['user_id'],
        context_type=event_data.get('context_type', 'general'),
        context_data=event_data.get('initial_context', {}),
        user_preferences=event_data.get('user_preferences', {})
    )