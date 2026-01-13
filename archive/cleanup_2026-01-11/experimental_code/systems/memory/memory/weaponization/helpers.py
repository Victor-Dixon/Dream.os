"""
Helper functions for memory weaponization
Re-exports functions from specialized modules for backward compatibility.
"""

# Import analytics functions
from .analytics_helpers import (
    get_date_range,
    extract_topics,
    detect_languages,
    calculate_daily_stats,
    calculate_agent_performance,
    calculate_conversation_trends
)

# Import content generation functions
from .content_helpers import (
    generate_blog_posts,
    generate_social_posts
)

# Import API functions
from .api_helpers import create_api_script

# Re-export all functions for backward compatibility
__all__ = [
    'get_date_range',
    'extract_topics',
    'detect_languages',
    'calculate_daily_stats',
    'calculate_agent_performance',
    'calculate_conversation_trends',
    'generate_blog_posts',
    'generate_social_posts',
    'create_api_script'
] 