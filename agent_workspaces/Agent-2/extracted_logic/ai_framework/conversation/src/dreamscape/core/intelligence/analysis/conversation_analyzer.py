#!/usr/bin/env python3
"""
Conversation Analyzer
====================

Analyzes conversation content and quality for the intelligence system.
"""

import logging
import re
from typing import Dict, List, Any, Optional
from datetime import datetime

from ..models.response_models import ResponseContext, ResponseAnalysis

logger = logging.getLogger(__name__)


class ConversationAnalyzer:
    """Analyzes conversation content and quality."""
    
    def __init__(self):
        """Initialize the conversation analyzer."""
        self.analysis_history = []
        logger.info("Conversation analyzer initialized")
    
    def analyze_response_quality(self, conversation_id: str, response_content: str,
                               conversation_content: str = "") -> Optional[ResponseAnalysis]:
        """
        Analyze the quality of a response.
        
        Args:
            conversation_id: ID of the conversation
            response_content: Content of the response to analyze
            conversation_content: Content of the original conversation
            
        Returns:
            Response analysis result
        """
        try:
            logger.info(f"Analyzing response quality for conversation: {conversation_id}")
            
            # Create response context
            context = ResponseContext(
                conversation_id=conversation_id,
                response_content=response_content,
                conversation_content=conversation_content,
                response_length=len(response_content),
                conversation_length=len(conversation_content),
                response_type=self._detect_response_type(response_content)
            )
            
            # Perform analysis
            analysis = self._perform_response_analysis(context)
            
            # Store analysis
            self.analysis_history.append(analysis)
            
            logger.info(f"Response analysis completed for conversation: {conversation_id}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing response for conversation {conversation_id}: {e}")
            return None
    
    def _detect_response_type(self, response_content: str) -> str:
        """Detect the type of response."""
        content_lower = response_content.lower()
        
        if '```' in response_content or 'def ' in content_lower or 'class ' in content_lower:
            return 'code'
        elif '?' in response_content and len(response_content.split('?')) > 2:
            return 'question'
        elif any(word in content_lower for word in ['suggest', 'recommend', 'try', 'consider']):
            return 'suggestion'
        elif any(word in content_lower for word in ['because', 'reason', 'explain', 'due to']):
            return 'explanation'
        else:
            return 'general'
    
    def _perform_response_analysis(self, context: ResponseContext) -> ResponseAnalysis:
        """Perform comprehensive response analysis."""
        # Calculate individual scores
        clarity_score = self._calculate_clarity_score(context)
        helpfulness_score = self._calculate_helpfulness_score(context)
        accuracy_score = self._calculate_accuracy_score(context)
        completeness_score = self._calculate_completeness_score(context)
        engagement_score = self._calculate_engagement_score(context)
        
        # Calculate overall score
        overall_score = (
            clarity_score * 0.2 +
            helpfulness_score * 0.3 +
            accuracy_score * 0.2 +
            completeness_score * 0.2 +
            engagement_score * 0.1
        )
        
        # Generate strengths and weaknesses
        strengths = self._identify_strengths(context, overall_score)
        weaknesses = self._identify_weaknesses(context, overall_score)
        suggestions = self._generate_suggestions(context, weaknesses)
        
        # Detect topics
        detected_topics = self._detect_topics(context)
        
        # Analyze sentiment
        sentiment = self._analyze_sentiment(context)
        
        return ResponseAnalysis(
            conversation_id=context.conversation_id,
            overall_score=overall_score,
            clarity_score=clarity_score,
            helpfulness_score=helpfulness_score,
            accuracy_score=accuracy_score,
            completeness_score=completeness_score,
            engagement_score=engagement_score,
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions,
            detected_topics=detected_topics,
            sentiment=sentiment,
            confidence_level=0.8,
            analysis_timestamp=datetime.now().isoformat()
        )
    
    def _calculate_clarity_score(self, context: ResponseContext) -> float:
        """Calculate clarity score for the response."""
        content = context.response_content
        
        # Factors that improve clarity
        clarity_factors = 0.0
        
        # Good sentence structure
        sentences = content.split('.')
        if len(sentences) > 1:
            clarity_factors += 0.2
        
        # Proper formatting
        if '\n' in content:
            clarity_factors += 0.1
        
        # Code blocks (if applicable)
        if '```' in content:
            clarity_factors += 0.2
        
        # Bullet points or lists
        if any(char in content for char in ['•', '-', '*', '1.', '2.']):
            clarity_factors += 0.1
        
        # Appropriate length
        if 50 <= len(content) <= 1000:
            clarity_factors += 0.2
        elif len(content) > 1000:
            clarity_factors += 0.1
        
        return min(1.0, clarity_factors)
    
    def _calculate_helpfulness_score(self, context: ResponseContext) -> float:
        """Calculate helpfulness score for the response."""
        content = context.response_content.lower()
        
        helpfulness_factors = 0.0
        
        # Actionable content
        if any(word in content for word in ['try', 'use', 'implement', 'add', 'create']):
            helpfulness_factors += 0.3
        
        # Explanatory content
        if any(word in content for word in ['because', 'reason', 'explain', 'due to']):
            helpfulness_factors += 0.2
        
        # Specific examples
        if any(word in content for word in ['example', 'instance', 'case', 'scenario']):
            helpfulness_factors += 0.2
        
        # Code examples
        if '```' in context.response_content:
            helpfulness_factors += 0.2
        
        # Links or references
        if 'http' in content or 'www.' in content:
            helpfulness_factors += 0.1
        
        return min(1.0, helpfulness_factors)
    
    def _calculate_accuracy_score(self, context: ResponseContext) -> float:
        """Calculate accuracy score for the response."""
        # This would typically involve more sophisticated analysis
        # For now, using a simple heuristic based on response characteristics
        
        content = context.response_content.lower()
        accuracy_factors = 0.5  # Base score
        
        # Technical terms suggest accuracy
        technical_terms = ['api', 'function', 'method', 'class', 'object', 'variable', 'parameter']
        tech_term_count = sum(1 for term in technical_terms if term in content)
        accuracy_factors += min(0.3, tech_term_count * 0.1)
        
        # Code blocks suggest technical accuracy
        if '```' in context.response_content:
            accuracy_factors += 0.2
        
        return min(1.0, accuracy_factors)
    
    def _calculate_completeness_score(self, context: ResponseContext) -> float:
        """Calculate completeness score for the response."""
        content = context.response_content
        completeness_factors = 0.0
        
        # Length factor
        if len(content) > 200:
            completeness_factors += 0.3
        elif len(content) > 100:
            completeness_factors += 0.2
        elif len(content) > 50:
            completeness_factors += 0.1
        
        # Multiple points covered
        sentences = content.split('.')
        if len(sentences) > 3:
            completeness_factors += 0.2
        
        # Code and explanation
        if '```' in content and len(content) > 100:
            completeness_factors += 0.2
        
        # Addresses the question
        if context.conversation_content and any(word in content.lower() 
                                               for word in context.conversation_content.lower().split()[:5]):
            completeness_factors += 0.3
        
        return min(1.0, completeness_factors)
    
    def _calculate_engagement_score(self, context: ResponseContext) -> float:
        """Calculate engagement score for the response."""
        content = context.response_content.lower()
        engagement_factors = 0.0
        
        # Questions encourage engagement
        if '?' in content:
            engagement_factors += 0.2
        
        # Personal pronouns
        if any(word in content for word in ['you', 'your', 'we', 'our']):
            engagement_factors += 0.2
        
        # Encouraging language
        if any(word in content for word in ['great', 'excellent', 'good', 'well', 'nice']):
            engagement_factors += 0.1
        
        # Interactive elements
        if any(word in content for word in ['try', 'test', 'check', 'verify']):
            engagement_factors += 0.2
        
        # Follow-up suggestions
        if any(word in content for word in ['next', 'also', 'additionally', 'furthermore']):
            engagement_factors += 0.1
        
        return min(1.0, engagement_factors)
    
    def _identify_strengths(self, context: ResponseContext, overall_score: float) -> List[str]:
        """Identify strengths in the response."""
        strengths = []
        content = context.response_content
        
        if overall_score >= 0.8:
            strengths.append("High overall quality")
        
        if len(content) > 200:
            strengths.append("Comprehensive response")
        
        if '```' in content:
            strengths.append("Includes code examples")
        
        if '\n' in content:
            strengths.append("Well-formatted")
        
        if '?' in content:
            strengths.append("Engaging and interactive")
        
        return strengths
    
    def _identify_weaknesses(self, context: ResponseContext, overall_score: float) -> List[str]:
        """Identify weaknesses in the response."""
        weaknesses = []
        content = context.response_content
        
        if overall_score < 0.6:
            weaknesses.append("Low overall quality")
        
        if len(content) < 50:
            weaknesses.append("Too brief")
        
        if len(content) > 1000:
            weaknesses.append("Too verbose")
        
        if not any(char in content for char in ['•', '-', '*', '1.', '2.']):
            if len(content) > 200:
                weaknesses.append("Could benefit from better structure")
        
        return weaknesses
    
    def _generate_suggestions(self, context: ResponseContext, weaknesses: List[str]) -> List[str]:
        """Generate improvement suggestions."""
        suggestions = []
        
        if "Too brief" in weaknesses:
            suggestions.append("Provide more detailed explanations")
        
        if "Too verbose" in weaknesses:
            suggestions.append("Be more concise and focused")
        
        if "Could benefit from better structure" in weaknesses:
            suggestions.append("Use bullet points or numbered lists")
        
        if "Low overall quality" in weaknesses:
            suggestions.append("Review and improve content quality")
        
        return suggestions
    
    def _detect_topics(self, context: ResponseContext) -> List[str]:
        """Detect topics in the response."""
        content = context.response_content.lower()
        topics = []
        
        # Programming topics
        if any(word in content for word in ['code', 'programming', 'function', 'class']):
            topics.append('programming')
        
        # Debugging topics
        if any(word in content for word in ['error', 'bug', 'debug', 'fix']):
            topics.append('debugging')
        
        # Design topics
        if any(word in content for word in ['design', 'architecture', 'structure']):
            topics.append('design')
        
        # Learning topics
        if any(word in content for word in ['learn', 'study', 'understand', 'explain']):
            topics.append('learning')
        
        return topics
    
    def _analyze_sentiment(self, context: ResponseContext) -> str:
        """Analyze sentiment of the response."""
        content = context.response_content.lower()
        
        positive_words = ['great', 'excellent', 'good', 'well', 'nice', 'helpful', 'useful']
        negative_words = ['bad', 'wrong', 'error', 'problem', 'issue', 'difficult']
        
        positive_count = sum(1 for word in positive_words if word in content)
        negative_count = sum(1 for word in negative_words if word in content)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def get_analysis_history(self) -> List[ResponseAnalysis]:
        """Get analysis history."""
        return self.analysis_history.copy()
    
    def clear_analysis_history(self):
        """Clear analysis history."""
        self.analysis_history.clear()
    
    def get_analysis_stats(self) -> Dict[str, Any]:
        """Get analysis statistics."""
        total_analyses = len(self.analysis_history)
        if total_analyses == 0:
            return {'total_analyses': 0}
        
        avg_overall_score = sum(a.overall_score for a in self.analysis_history) / total_analyses
        avg_clarity_score = sum(a.clarity_score for a in self.analysis_history) / total_analyses
        avg_helpfulness_score = sum(a.helpfulness_score for a in self.analysis_history) / total_analyses
        
        return {
            'total_analyses': total_analyses,
            'avg_overall_score': avg_overall_score,
            'avg_clarity_score': avg_clarity_score,
            'avg_helpfulness_score': avg_helpfulness_score
        } 