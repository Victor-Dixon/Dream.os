#!/usr/bin/env python3
"""
Memory Content Processor
=======================

Processes and analyzes conversation content for memory storage.
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class MemoryContentProcessor:
    """Processes and analyzes conversation content for memory storage."""
    
    def __init__(self, storage):
        self.storage = storage
    
    def process_conversation(self, conversation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a conversation for memory storage."""
        processed = {
            'id': conversation_data.get('id'),
            'title': conversation_data.get('title', 'Untitled'),
            'timestamp': conversation_data.get('timestamp'),
            'messages': conversation_data.get('messages', []),
            'message_count': len(conversation_data.get('messages', [])),
            'content_summary': self._extract_summary(conversation_data),
            'topics': self._extract_topics(conversation_data),
            'sentiment': self._analyze_sentiment(conversation_data)
        }
        return processed
    
    def _extract_summary(self, conversation_data: Dict[str, Any]) -> str:
        """Extract a summary of the conversation."""
        messages = conversation_data.get('messages', [])
        if not messages:
            return ""
        
        # Simple summary: first few messages
        summary_parts = []
        for msg in messages[:3]:
            content = msg.get('content', '')[:100]
            if content:
                summary_parts.append(content)
        
        return " | ".join(summary_parts)
    
    def _extract_topics(self, conversation_data: Dict[str, Any]) -> List[str]:
        """Extract topics from conversation."""
        # Simple topic extraction based on keywords
        content = self._extract_content(conversation_data)
        topics = []
        
        # Add basic topic detection logic here
        if 'code' in content.lower() or 'programming' in content.lower():
            topics.append('programming')
        if 'ai' in content.lower() or 'artificial intelligence' in content.lower():
            topics.append('ai')
        if 'game' in content.lower() or 'gaming' in content.lower():
            topics.append('gaming')
        
        return topics
    
    def _analyze_sentiment(self, conversation_data: Dict[str, Any]) -> str:
        """Analyze sentiment of conversation."""
        # Simple sentiment analysis
        content = self._extract_content(conversation_data).lower()
        
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disappointing']
        
        positive_count = sum(1 for word in positive_words if word in content)
        negative_count = sum(1 for word in negative_words if word in content)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _extract_content(self, conversation_data: Dict[str, Any]) -> str:
        """Extract all text content from conversation."""
        messages = conversation_data.get('messages', [])
        content_parts = []
        
        for msg in messages:
            content = msg.get('content', '')
            if content:
                content_parts.append(content)
        
        return ' '.join(content_parts) 