"""
Analytics helper functions for memory weaponization
Handles data analysis and statistics calculations.
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

def get_date_range(conversations: List[Dict]) -> Dict[str, str]:
    """
    Get date range of conversations.
    
    Args:
        conversations: List of conversation dictionaries
        
    Returns:
        Dictionary with start and end dates
    """
    timestamps = [conv.get('timestamp') for conv in conversations if conv.get('timestamp')]
    if timestamps:
        return {"start": min(timestamps), "end": max(timestamps)}
    return {"start": "", "end": ""}

def extract_topics(conversations: List[Dict]) -> List[str]:
    """
    Extract common topics from conversations.
    
    Args:
        conversations: List of conversation dictionaries
        
    Returns:
        List of unique topics
    """
    topics = set()
    for conv in conversations:
        conv_topics = conv.get('topics', [])
        if isinstance(conv_topics, list):
            topics.update(conv_topics)
    return list(topics)

def detect_languages(conversations: List[Dict]) -> List[str]:
    """
    Detect programming languages used in conversations.
    
    Args:
        conversations: List of conversation dictionaries
        
    Returns:
        List of detected programming languages
    """
    languages = set()
    for conv in conversations:
        content = ' '.join([msg.get('content', '') for msg in conv.get('messages', [])])
        content_lower = content.lower()
        
        if 'python' in content_lower:
            languages.add('Python')
        if 'javascript' in content_lower:
            languages.add('JavaScript')
        if 'java' in content_lower:
            languages.add('Java')
        if 'typescript' in content_lower:
            languages.add('TypeScript')
        if 'c++' in content_lower or 'cpp' in content_lower:
            languages.add('C++')
        if 'c#' in content_lower or 'csharp' in content_lower:
            languages.add('C#')
        if 'go' in content_lower:
            languages.add('Go')
        if 'rust' in content_lower:
            languages.add('Rust')
        if 'php' in content_lower:
            languages.add('PHP')
        if 'ruby' in content_lower:
            languages.add('Ruby')
    
    return list(languages)

def calculate_daily_stats(conversations: List[Dict]) -> Dict[str, Any]:
    """
    Calculate daily conversation statistics.
    
    Args:
        conversations: List of conversation dictionaries
        
    Returns:
        Dictionary with daily statistics
    """
    if not conversations:
        return {"total_days": 0, "avg_conversations_per_day": 0}
    
    # Extract dates from timestamps
    dates = []
    for conv in conversations:
        timestamp = conv.get('timestamp', '')
        if timestamp and len(timestamp) >= 10:
            date = timestamp[:10]  # YYYY-MM-DD format
            dates.append(date)
    
    if not dates:
        return {"total_days": 0, "avg_conversations_per_day": 0}
    
    unique_dates = set(dates)
    total_days = len(unique_dates)
    avg_conversations_per_day = len(conversations) / total_days if total_days > 0 else 0
    
    return {
        "total_days": total_days,
        "avg_conversations_per_day": round(avg_conversations_per_day, 2),
        "date_range": get_date_range(conversations)
    }

def calculate_agent_performance(conversations: List[Dict]) -> Dict[str, Any]:
    """
    Calculate agent performance metrics.
    
    Args:
        conversations: List of conversation dictionaries
        
    Returns:
        Dictionary with performance metrics
    """
    if not conversations:
        return {"total_messages": 0, "avg_messages_per_conversation": 0}
    
    total_messages = 0
    user_messages = 0
    assistant_messages = 0
    
    for conv in conversations:
        messages = conv.get('messages', [])
        total_messages += len(messages)
        
        for msg in messages:
            role = msg.get('role', '').lower()
            if role == 'user':
                user_messages += 1
            elif role == 'assistant':
                assistant_messages += 1
    
    avg_messages_per_conversation = total_messages / len(conversations) if conversations else 0
    
    return {
        "total_messages": total_messages,
        "user_messages": user_messages,
        "assistant_messages": assistant_messages,
        "avg_messages_per_conversation": round(avg_messages_per_conversation, 2),
        "total_conversations": len(conversations)
    }

def calculate_conversation_trends(conversations: List[Dict]) -> Dict[str, Any]:
    """
    Calculate conversation trends.
    
    Args:
        conversations: List of conversation dictionaries
        
    Returns:
        Dictionary with trend analysis
    """
    if not conversations:
        return {"trend": "no_data", "growth_rate": 0}
    
    # Sort conversations by timestamp
    sorted_convs = sorted(conversations, key=lambda x: x.get('timestamp', ''))
    
    if len(sorted_convs) < 2:
        return {"trend": "insufficient_data", "growth_rate": 0}
    
    # Calculate simple trend based on message count over time
    first_half = sorted_convs[:len(sorted_convs)//2]
    second_half = sorted_convs[len(sorted_convs)//2:]
    
    first_half_messages = sum(len(conv.get('messages', [])) for conv in first_half)
    second_half_messages = sum(len(conv.get('messages', [])) for conv in second_half)
    
    if first_half_messages == 0:
        growth_rate = 100 if second_half_messages > 0 else 0
    else:
        growth_rate = ((second_half_messages - first_half_messages) / first_half_messages) * 100
    
    if growth_rate > 10:
        trend = "increasing"
    elif growth_rate < -10:
        trend = "decreasing"
    else:
        trend = "stable"
    
    return {
        "trend": trend,
        "growth_rate": round(growth_rate, 2),
        "first_half_messages": first_half_messages,
        "second_half_messages": second_half_messages
    } 