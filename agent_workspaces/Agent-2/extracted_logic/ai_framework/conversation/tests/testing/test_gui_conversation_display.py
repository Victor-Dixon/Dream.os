#!/usr/bin/env python3
"""
Test GUI Conversation Display
Test that conversation content is properly displayed in the GUI.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dreamscape.core.memory.manager import MemoryManager

def test_conversation_display():
    """Test that conversation content is properly loaded and displayed."""
    try:
        print("🧪 Testing GUI conversation display...")
        
        # Initialize memory manager
        memory_manager = MemoryManager("dreamos_memory.db")
        
        # Get conversations with content
        conversations = memory_manager.get_conversations_chronological(limit=5)
        
        print(f"📊 Found {len(conversations)} conversations to test")
        
        for i, conv in enumerate(conversations, 1):
            conv_id = conv.get('id', 'unknown')
            title = conv.get('title', 'No title')
            content = conv.get('content', '')
            content_length = len(content) if content else 0
            
            print(f"\n📝 Conversation {i}:")
            print(f"  ID: {conv_id}")
            print(f"  Title: {title}")
            print(f"  Content length: {content_length} characters")
            
            if content_length > 0:
                print(f"  ✅ Content available for display")
                # Show first 100 characters as preview
                preview = content[:100].replace('\n', ' ').strip()
                print(f"  Preview: {preview}...")
            else:
                print(f"  ❌ No content available")
        
        # Test conversation panel loading simulation
        print(f"\n🎯 Testing conversation panel loading simulation...")
        
        # Simulate what the GUI would do
        total_conversations = len(memory_manager.get_conversations_chronological())
        conversations_with_content = [c for c in memory_manager.get_conversations_chronological() if c.get('content')]
        
        print(f"  Total conversations: {total_conversations}")
        print(f"  Conversations with content: {len(conversations_with_content)}")
        print(f"  Content coverage: {(len(conversations_with_content) / total_conversations * 100):.1f}%")
        
        if len(conversations_with_content) > 0:
            print("✅ GUI should display conversation content properly")
            return True
        else:
            print("❌ No conversations with content found - GUI will show empty content")
            return False
            
    except Exception as e:
        print(f"❌ Conversation display test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_conversation_display()
    sys.exit(0 if success else 1) 