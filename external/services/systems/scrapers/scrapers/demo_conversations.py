"""
Demo Conversation Generator
Handles generation of demo conversations for testing and offline flows.
"""

import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

class DemoConversationGenerator:
    """Handles generation of demo conversations for testing and offline flows."""
    
    @staticmethod
    def get_demo_conversations(limit: int = 5) -> List[Dict[str, str]]:
        """
        Return a small set of demo conversations for offline/testing flows.

        Priority:
        1. Pull the most recent conversations from the Dreamscape memory DB (if available)
           so demos stay realistic.
        2. Fallback to a static synthetic list if the DB is empty or unavailable.
        
        Args:
            limit: Maximum number of demo conversations to return
            
        Returns:
            List of demo conversation dictionaries
        """
        try:
            from dreamscape.core.memory_api import get_memory_api
            api = get_memory_api()
            recent = api.get_recent_conversations(limit)
            if recent:
                # Massage to expected shape for examples/tests
                return [
                    {
                        "id": conv["id"],
                        "title": conv.get("title", "Untitled"),
                        "url": conv.get("url", f"https://chat.openai.com/c/{conv['id']}"),
                        "timestamp": conv.get("timestamp", ""),
                        "captured_at": conv.get("timestamp", ""),
                    }
                    for conv in recent
                ]
        except Exception:
            # Memory not ready — fall through to static examples
            pass

        # Static fallback (ensures self-contained demo)
        return DemoConversationGenerator._get_static_demo_conversations(limit)
    
    @staticmethod
    def _get_static_demo_conversations(limit: int = 5) -> List[Dict[str, str]]:
        """
        Generate static demo conversations for fallback scenarios.
        
        Args:
            limit: Number of demo conversations to generate
            
        Returns:
            List of static demo conversation dictionaries
        """
        now = datetime.utcnow().isoformat()
        return [
            {
                "id": f"demo_{i+1}",
                "title": f"Demo Conversation {i+1}",
                "url": f"https://chat.openai.com/c/demo_{i+1}",
                "timestamp": now,
                "captured_at": now,
            }
            for i in range(limit)
        ] 