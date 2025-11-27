#!/usr/bin/env python3
"""
Debug script to check conversation content fields.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# EDIT START: Consolidate memory imports to use memory_system (core consolidation)
from dreamscape.core.memory import get_memory_api
# EDIT END

def debug_conversation_content():
    """Debug conversation content fields."""
    try:
        
        print("🔍 Debugging conversation content...")
        
        # Get memory API
        api = get_memory_api()
        
        # Get total count
        total_count = api.get_conversations_count()
        print(f"📊 Total conversations in database: {total_count}")
        
        # Get conversations with message counts > 0
        print("\n🔍 Looking for conversations with actual content...")
        all_conversations = api.get_conversations_chronological(limit=100)
        
        conversations_with_content = []
        conversations_without_content = []
        
        for conv in all_conversations:
            message_count = conv.get('message_count', 0)
            content = conv.get('content', '')
            
            if message_count > 0 or (content and len(content) > 10):
                conversations_with_content.append(conv)
            else:
                conversations_without_content.append(conv)
        
        print(f"✅ Conversations with content: {len(conversations_with_content)}")
        print(f"❌ Conversations without content: {len(conversations_without_content)}")
        
        # Show conversations with content
        if conversations_with_content:
            print(f"\n📋 Conversations with content (showing first 3):")
            for i, conv in enumerate(conversations_with_content[:3], 1):
                print(f"\n--- Conversation {i} ---")
                print(f"ID: {conv.get('id', 'unknown')}")
                print(f"Title: {conv.get('title', 'Untitled')}")
                print(f"Message Count: {conv.get('message_count', 0)}")
                print(f"Word Count: {conv.get('word_count', 0)}")
                
                content = conv.get('content', '')
                if content:
                    print(f"Content Length: {len(content)} characters")
                    print(f"Content Preview: {content[:200]}...")
                
                # Get full conversation details
                full_conv = api.get_conversation(conv.get('id'))
                if full_conv and full_conv.get('content'):
                    print(f"✅ Full conversation has content: {len(full_conv['content'])} characters")
                else:
                    print("❌ Full conversation has no content")
        else:
            print("\n❌ No conversations with content found!")
            print("💡 This means the conversations were imported but their content wasn't extracted.")
            print("💡 You may need to:")
            print("   1. Import conversation JSON files with actual content")
            print("   2. Use the scraper to extract content from ChatGPT")
            print("   3. Process existing conversations to extract content")
        
        # Check for demo conversations specifically
        print(f"\n🔍 Checking for demo conversations...")
        demo_conversations = [conv for conv in all_conversations if 'demo' in conv.get('id', '').lower()]
        if demo_conversations:
            print(f"✅ Found {len(demo_conversations)} demo conversations")
            for conv in demo_conversations:
                print(f"  - {conv.get('title', 'Untitled')} (ID: {conv.get('id')})")
                content = conv.get('content', '')
                if content:
                    print(f"    Content: {len(content)} characters")
                else:
                    print(f"    No content")
        else:
            print("❌ No demo conversations found")
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_conversation_content() 