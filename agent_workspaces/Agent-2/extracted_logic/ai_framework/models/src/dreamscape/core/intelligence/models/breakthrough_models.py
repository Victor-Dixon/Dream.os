#!/usr/bin/env python3
"""
Breakthrough Models
==================

Data models for breakthrough detection intelligence features.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class BreakthroughAnalysis:
    """Analysis of potential breakthroughs in conversation."""
    conversation_id: str
    breakthrough_detected: bool
    breakthrough_type: str = "none"  # 'insight', 'discovery', 'solution', 'innovation'
    confidence_score: float = 0.0
    breakthrough_description: str = ""
    key_insights: List[str] = field(default_factory=list)
    potential_impact: str = "low"  # 'low', 'medium', 'high', 'critical'
    related_concepts: List[str] = field(default_factory=list)
    suggested_actions: List[str] = field(default_factory=list)
    detection_timestamp: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert analysis to dictionary."""
        return {
            'conversation_id': self.conversation_id,
            'breakthrough_detected': self.breakthrough_detected,
            'breakthrough_type': self.breakthrough_type,
            'confidence_score': self.confidence_score,
            'breakthrough_description': self.breakthrough_description,
            'key_insights': self.key_insights,
            'potential_impact': self.potential_impact,
            'related_concepts': self.related_concepts,
            'suggested_actions': self.suggested_actions,
            'detection_timestamp': self.detection_timestamp,
            'metadata': self.metadata
        }
    
    def is_significant(self) -> bool:
        """Check if breakthrough is significant."""
        return (
            self.breakthrough_detected and
            self.confidence_score >= 0.7 and
            self.potential_impact in ['high', 'critical']
        )
    
    def is_moderate(self) -> bool:
        """Check if breakthrough is moderate."""
        return (
            self.breakthrough_detected and
            self.confidence_score >= 0.5 and
            self.potential_impact in ['medium', 'high']
        )
    
    def get_impact_score(self) -> int:
        """Get numerical impact score."""
        impact_scores = {
            'low': 1,
            'medium': 2,
            'high': 3,
            'critical': 4
        }
        return impact_scores.get(self.potential_impact, 1)
    
    def get_primary_insight(self) -> Optional[str]:
        """Get the primary insight from the breakthrough."""
        if self.key_insights:
            return self.key_insights[0]
        return None
    
    def get_primary_action(self) -> Optional[str]:
        """Get the primary suggested action."""
        if self.suggested_actions:
            return self.suggested_actions[0]
        return None 