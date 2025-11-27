#!/usr/bin/env python3
"""
Test script to list available conversations.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dreamscape.core.memory.manager import MemoryManager

def main():
    """List available conversations."""
    print("📋 Listing available conversations...")
    
    try:
        memory_manager = MemoryManager("dreamos_memory.db")
        
        # Get conversations in chronological order
        conversations = memory_manager.get_conversations_chronological(limit=10)
        
        print(f"\n📊 Found {len(conversations)} conversations:")
        print("-" * 80)
        
        for i, conv in enumerate(conversations, 1):
            content_length = len(conv.get('content', ''))
            has_content = "✅" if content_length > 100 else "❌"
            source = conv.get('source', 'unknown')
            
            print(f"{i:2d}. {conv['id']} - {conv['title']}")
            print(f"     Content: {has_content} ({content_length} chars)")
            print(f"     Source: {source}")
            print(f"     Messages: {conv.get('message_count', 0)}")
            print(f"     Words: {conv.get('word_count', 0)}")
            print(f"     Date: {conv.get('timestamp', 'unknown')}")
            print()
        
        # Also check total count
        total_count = memory_manager.get_conversations_count()
        print(f"📈 Total conversations in database: {total_count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 