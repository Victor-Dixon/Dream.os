"""
Content generation helper functions for memory weaponization
Handles blog post and social media content generation.
"""

import logging
from typing import Dict, List, Any
from .analytics_helpers import extract_topics, detect_languages

logger = logging.getLogger(__name__)

def generate_blog_posts(conversations: List[Dict]) -> List[Dict]:
    """
    Generate blog posts from conversations.
    
    Args:
        conversations: List of conversation dictionaries
        
    Returns:
        List of blog post dictionaries
    """
    if not conversations:
        return []
    
    # Extract topics for blog post generation
    topics = extract_topics(conversations)
    languages = detect_languages(conversations)
    
    blog_posts = []
    
    # Generate blog post about most common topic
    if topics:
        main_topic = topics[0] if topics else "AI Development"
        blog_posts.append({
            "title": f"Exploring {main_topic}: Insights from Recent Conversations",
            "content": f"A deep dive into {main_topic} based on our recent AI interactions.",
            "topics": topics[:3],  # Top 3 topics
            "word_count": 800
        })
    
    # Generate blog post about programming languages
    if languages:
        blog_posts.append({
            "title": f"Programming Languages in AI Conversations: {', '.join(languages)}",
            "content": f"Analysis of programming language usage in our AI conversations.",
            "languages": languages,
            "word_count": 600
        })
    
    return blog_posts

def generate_social_posts(conversations: List[Dict]) -> List[Dict]:
    """
    Generate social media posts from conversations.
    
    Args:
        conversations: List of conversation dictionaries
        
    Returns:
        List of social media post dictionaries
    """
    if not conversations:
        return []
    
    topics = extract_topics(conversations)
    languages = detect_languages(conversations)
    
    social_posts = []
    
    # Twitter-style posts
    if topics:
        social_posts.append({
            "platform": "twitter",
            "content": f"🚀 Excited to share insights on {topics[0]} from our AI conversations! #AI #Development",
            "hashtags": ["#AI", "#Development", "#Innovation"]
        })
    
    if languages:
        social_posts.append({
            "platform": "twitter",
            "content": f"💻 Exploring {', '.join(languages[:2])} in AI conversations. The future of programming is here!",
            "hashtags": ["#Programming", "#AI", "#Tech"]
        })
    
    # LinkedIn-style posts
    social_posts.append({
        "platform": "linkedin",
        "content": f"Professional insights from {len(conversations)} AI conversations. Key topics: {', '.join(topics[:3])}",
        "hashtags": ["#AI", "#ProfessionalDevelopment", "#Innovation"]
    })
    
    return social_posts 