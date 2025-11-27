#!/usr/bin/env python3
"""
Response Models
==============

Data models for response analysis intelligence features.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class ResponseContext:
    """Context information for response analysis."""
    conversation_id: str
    response_content: str
    conversation_content: str
    response_length: int = 0
    conversation_length: int = 0
    response_type: str = "general"  # 'code', 'explanation', 'question', 'suggestion'
    user_feedback: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary."""
        return {
            'conversation_id': self.conversation_id,
            'response_content': self.response_content,
            'conversation_content': self.conversation_content,
            'response_length': self.response_length,
            'conversation_length': self.conversation_length,
            'response_type': self.response_type,
            'user_feedback': self.user_feedback,
            'metadata': self.metadata
        }


@dataclass
class ResponseAnalysis:
    """Analysis of response quality and characteristics."""
    conversation_id: str
    overall_score: float  # 0.0 to 1.0
    clarity_score: float
    helpfulness_score: float
    accuracy_score: float
    completeness_score: float
    engagement_score: float
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    detected_topics: List[str] = field(default_factory=list)
    sentiment: str = "neutral"  # 'positive', 'negative', 'neutral'
    confidence_level: float = 0.0
    analysis_timestamp: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert analysis to dictionary."""
        return {
            'conversation_id': self.conversation_id,
            'overall_score': self.overall_score,
            'clarity_score': self.clarity_score,
            'helpfulness_score': self.helpfulness_score,
            'accuracy_score': self.accuracy_score,
            'completeness_score': self.completeness_score,
            'engagement_score': self.engagement_score,
            'strengths': self.strengths,
            'weaknesses': self.weaknesses,
            'suggestions': self.suggestions,
            'detected_topics': self.detected_topics,
            'sentiment': self.sentiment,
            'confidence_level': self.confidence_level,
            'analysis_timestamp': self.analysis_timestamp,
            'metadata': self.metadata
        }
    
    def is_high_quality(self) -> bool:
        """Check if response is considered high quality."""
        return self.overall_score >= 0.8
    
    def is_acceptable(self) -> bool:
        """Check if response is acceptable quality."""
        return self.overall_score >= 0.6
    
    def needs_improvement(self) -> bool:
        """Check if response needs improvement."""
        return self.overall_score < 0.6
    
    def get_primary_issue(self) -> Optional[str]:
        """Get the primary issue with the response."""
        if self.weaknesses:
            return self.weaknesses[0]
        return None
    
    def get_improvement_suggestion(self) -> Optional[str]:
        """Get the most important improvement suggestion."""
        if self.suggestions:
            return self.suggestions[0]
        return None 