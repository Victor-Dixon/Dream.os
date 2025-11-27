#!/usr/bin/env python3
"""
Processing Models
================

Data models for live processing intelligence features.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class ProcessingEvent:
    """Event generated during live processing."""
    event_id: str
    event_type: str  # 'quest_generated', 'xp_awarded', 'breakthrough_detected', 'response_analyzed'
    conversation_id: str
    timestamp: str
    event_data: Dict[str, Any] = field(default_factory=dict)
    priority: str = "normal"  # 'low', 'normal', 'high', 'critical'
    processed: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary."""
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'conversation_id': self.conversation_id,
            'timestamp': self.timestamp,
            'event_data': self.event_data,
            'priority': self.priority,
            'processed': self.processed,
            'metadata': self.metadata
        }
    
    def is_high_priority(self) -> bool:
        """Check if event is high priority."""
        return self.priority in ['high', 'critical']
    
    def is_critical(self) -> bool:
        """Check if event is critical priority."""
        return self.priority == 'critical'
    
    def get_priority_score(self) -> int:
        """Get numerical priority score."""
        priority_scores = {
            'low': 1,
            'normal': 2,
            'high': 3,
            'critical': 4
        }
        return priority_scores.get(self.priority, 2)
    
    def mark_processed(self):
        """Mark event as processed."""
        self.processed = True
    
    def is_quest_event(self) -> bool:
        """Check if event is quest-related."""
        return self.event_type in ['quest_generated', 'quest_completed', 'quest_failed']
    
    def is_xp_event(self) -> bool:
        """Check if event is XP-related."""
        return self.event_type in ['xp_awarded', 'xp_bonus', 'level_up']
    
    def is_breakthrough_event(self) -> bool:
        """Check if event is breakthrough-related."""
        return self.event_type in ['breakthrough_detected', 'insight_found', 'discovery_made']
    
    def is_response_event(self) -> bool:
        """Check if event is response-related."""
        return self.event_type in ['response_analyzed', 'response_improved', 'feedback_received'] 